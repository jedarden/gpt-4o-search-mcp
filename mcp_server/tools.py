# Tools module for MCP server

from mcp_server.openai_client import search_openai, stream_search_openai
from mcp_server.config import get_settings
import re

async def web_search_tool(query: str, stream: bool = False):
    """
    Web search tool that calls OpenAI API with the gpt-4o-search-preview model.
    Validates input, handles errors, and returns structured results.
    Supports streaming (SSE) if stream=True.
    """
    # Input validation
    if not isinstance(query, str):
        return {"success": False, "error": "Query must be a string."}
    query = query.strip()
    if not query:
        return {"success": False, "error": "Query cannot be empty."}
    if len(query) > 512:
        return {"success": False, "error": "Query too long (max 512 characters)."}

    # Optional: sanitize input (basic, for demonstration)
    if re.search(r"[\x00-\x08\x0B\x0C\x0E-\x1F]", query):
        return {"success": False, "error": "Query contains invalid control characters."}

    # Load API key securely
    settings = get_settings()
    api_key = settings.get("OPENAI_API_KEY")
    if not api_key:
        return {"success": False, "error": "OpenAI API key not configured."}

    if stream:
        # Return an async generator for SSE streaming
        async def sse_generator():
            async for chunk in stream_search_openai(query, api_key):
                # Never expose API key in result
                if "api_key" in chunk:
                    del chunk["api_key"]
                yield chunk
        return sse_generator()
    else:
        # Call OpenAI API (non-streaming)
        result = await search_openai(query, api_key)
        # Never expose API key in result
        if "api_key" in result:
            del result["api_key"]
        return result