# OpenAI API integration for MCP server (using official OpenAI SDK)

import openai
import asyncio

OPENAI_MODEL = "gpt-4o-search-preview"

async def search_openai(query: str, api_key: str):
    """
    Calls the OpenAI API with the gpt-4o-search-preview model using the official SDK.
    Returns a dict with the search results or error details.
    """
    try:
        client = openai.AsyncOpenAI(api_key=api_key)
        response = await client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful web search assistant."},
                {"role": "user", "content": query}
            ],
            max_tokens=512,
            temperature=0.2,
            stream=False,
        )
        # Extract the main result from the response
        result = response.choices[0].message.content if response.choices else ""
        return {"success": True, "result": result}
    except openai.OpenAIError as e:
        return {
            "success": False,
            "error": "OpenAI API error",
            "details": str(e)
        }
    except Exception as e:
        return {
            "success": False,
            "error": "Unexpected error",
            "details": str(e)
        }

async def stream_search_openai(query: str, api_key: str):
    """
    Async generator that streams tokens from the OpenAI API using the official SDK.
    Yields dicts with incremental results for SSE.
    """
    try:
        client = openai.AsyncOpenAI(api_key=api_key)
        stream = await client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful web search assistant."},
                {"role": "user", "content": query}
            ],
            max_tokens=512,
            temperature=0.2,
            stream=True,
        )
        async for chunk in stream:
            # Each chunk is an OpenAI object with delta content
            delta = chunk.choices[0].delta.content if chunk.choices and chunk.choices[0].delta else None
            if delta:
                yield {"success": True, "delta": delta}
        # Signal end of stream
        yield {"success": True, "done": True}
    except openai.OpenAIError as e:
        yield {
            "success": False,
            "error": "OpenAI API error",
            "details": str(e)
        }
    except Exception as e:
        yield {
            "success": False,
            "error": "Unexpected error",
            "details": str(e)
        }