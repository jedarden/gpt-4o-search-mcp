import asyncio
import json
from mcp.client.sse import create_mcp_http_client

async def main():
    url = "http://localhost:8000/sse"
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "call_tool",
        "params": {
            "tool": "search",
            "args": {"query": "What is Model Context Protocol?"}
        }
    }
    async with create_mcp_http_client() as client:
        response = await client.post(url, json=payload)
        try:
            data = response.json()
        except Exception:
            data = response.text
        print("Search result:", data)

if __name__ == "__main__":
    asyncio.run(main())