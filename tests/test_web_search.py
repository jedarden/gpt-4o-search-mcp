"""
Test suite for the MCP server web search tool.

Covers:
- Valid search queries (typical, long, special characters)
- Missing or invalid queries (empty, non-string)
- OpenAI API errors (network failure, invalid API key, rate limiting)
- Security (API key never exposed)
- Edge cases and negative scenarios

Uses Arrange-Act-Assert pattern.
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient
import asyncio


from mcp_server.main import app
from unittest.mock import patch, AsyncMock, MagicMock

@pytest.mark.asyncio
async def test_valid_search_query(monkeypatch):
    async def mock_search_openai(query, api_key):
        return {"success": True, "result": "Search result for: " + query}
    # Patch the tool to use the mock
    app.tools[0].__globals__["search_openai"] = mock_search_openai

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/tools/web_search_tool", json={"query": "What is AI?"})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "result" in data
        assert "AI" in data["result"]

@pytest.mark.asyncio
async def test_long_search_query(monkeypatch):
    async def mock_search_openai(query, api_key):
        return {"success": True, "result": "ok"}
    app.tools[0].__globals__["search_openai"] = mock_search_openai

    long_query = "a" * 512
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/tools/web_search_tool", json={"query": long_query})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

@pytest.mark.asyncio
async def test_special_characters_query(monkeypatch):
    async def mock_search_openai(query, api_key):
        return {"success": True, "result": "ok"}
    app.tools[0].__globals__["search_openai"] = mock_search_openai

    special_query = "!@#$%^&*()_+-=[]{}|;':,.<>/?"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/tools/web_search_tool", json={"query": special_query})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

@pytest.mark.asyncio
async def test_missing_query():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/tools/web_search_tool", json={})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "error" in data

@pytest.mark.asyncio
async def test_empty_query():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/tools/web_search_tool", json={"query": ""})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "error" in data

@pytest.mark.asyncio
async def test_non_string_query():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/tools/web_search_tool", json={"query": 123})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "error" in data

@pytest.mark.asyncio
async def test_openai_api_network_failure(monkeypatch):
    async def mock_search_openai(query, api_key):
        return {"success": False, "error": "Network error", "details": "Simulated network failure"}
    app.tools[0].__globals__["search_openai"] = mock_search_openai

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/tools/web_search_tool", json={"query": "test"})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert data["error"] == "Network error"

@pytest.mark.asyncio
async def test_openai_api_invalid_key(monkeypatch):
    async def mock_search_openai(query, api_key):
        return {"success": False, "error": "OpenAI API error: 401", "details": "Invalid API key"}
    app.tools[0].__globals__["search_openai"] = mock_search_openai

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/tools/web_search_tool", json={"query": "test"})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "401" in data["error"]

@pytest.mark.asyncio
async def test_openai_api_rate_limit(monkeypatch):
    async def mock_search_openai(query, api_key):
        return {"success": False, "error": "OpenAI API error: 429", "details": "Rate limit exceeded"}
    app.tools[0].__globals__["search_openai"] = mock_search_openai

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/tools/web_search_tool", json={"query": "test"})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "429" in data["error"]

@pytest.mark.asyncio
async def test_api_key_never_exposed(monkeypatch):
    async def mock_search_openai(query, api_key):
        return {"success": True, "result": "ok", "api_key": "should_not_be_here"}
    app.tools[0].__globals__["search_openai"] = mock_search_openai

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/tools/web_search_tool", json={"query": "test"})
        assert response.status_code == 200
        data = response.json()
        assert "api_key" not in data

@pytest.mark.asyncio
async def test_streaming_valid_query(monkeypatch):
    # Mock OpenAI streaming: yields two deltas and a done
    async def mock_stream_search_openai(query, api_key):
        yield {"success": True, "delta": "Hello"}
        yield {"success": True, "delta": " world"}
        yield {"success": True, "done": True}
    app.tools[0].__globals__["stream_search_openai"] = mock_stream_search_openai

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/tools/web_search_tool", json={"query": "stream test", "stream": True})
        # The response is an async generator (SSE simulation)
        # We need to consume the generator
        results = []
        async for chunk in response.aiter_json():
            results.append(chunk)
        # Should see two deltas and a done
        assert any("delta" in c and c["delta"] == "Hello" for c in results)
        assert any("delta" in c and c["delta"] == " world" for c in results)
        assert any("done" in c and c["done"] is True for c in results)

@pytest.mark.asyncio
async def test_streaming_openai_error(monkeypatch):
    # Mock OpenAI streaming: yields an error
    async def mock_stream_search_openai(query, api_key):
        yield {"success": False, "error": "OpenAI API error", "details": "Simulated error"}
    app.tools[0].__globals__["stream_search_openai"] = mock_stream_search_openai

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/tools/web_search_tool", json={"query": "stream test", "stream": True})
        results = [chunk async for chunk in response.aiter_json()]
        assert any(c.get("success") is False and "error" in c for c in results)

@pytest.mark.asyncio
async def test_streaming_missing_query():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/tools/web_search_tool", json={"stream": True})
        # Should return a single error chunk
        results = [chunk async for chunk in response.aiter_json()]
        assert any(c.get("success") is False and "error" in c for c in results)

@pytest.mark.asyncio
async def test_streaming_non_string_query():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/tools/web_search_tool", json={"query": 123, "stream": True})
        results = [chunk async for chunk in response.aiter_json()]
        assert any(c.get("success") is False and "error" in c for c in results)

@pytest.mark.asyncio
async def test_openai_sdk_used_for_completions_and_streaming():
    # Patch openai.AsyncOpenAI for both search_openai and stream_search_openai
    with patch("mcp_server.openai_client.openai.AsyncOpenAI") as mock_async_openai:
        # Setup mock for completions
        mock_client = MagicMock()
        mock_chat = MagicMock()
        mock_completions = MagicMock()
        mock_create = AsyncMock()
        # For non-streaming: returns a response with choices
        mock_create.return_value = MagicMock(choices=[MagicMock(message=MagicMock(content="mocked result"))])
        mock_completions.create = mock_create
        mock_chat.completions = mock_completions
        mock_client.chat = mock_chat
        mock_async_openai.return_value = mock_client

        # Test non-streaming
        from mcp_server.openai_client import search_openai
        result = asyncio.run(search_openai("test", "sk-test"))
        assert result["success"] is True
        mock_create.assert_awaited_once()
        # Test streaming: returns an async generator
        async def async_gen():
            yield MagicMock(choices=[MagicMock(delta=MagicMock(content="delta1"))])
            yield MagicMock(choices=[MagicMock(delta=MagicMock(content="delta2"))])
        mock_create.return_value = async_gen()
        from mcp_server.openai_client import stream_search_openai
        async def run_stream():
            results = []
            async for chunk in stream_search_openai("test", "sk-test"):
                results.append(chunk)
            return results
        results = asyncio.run(run_stream())
        assert any("delta" in c and c["delta"] == "delta1" for c in results)
        assert any("delta" in c and c["delta"] == "delta2" for c in results)
        assert mock_create.await_count >= 1