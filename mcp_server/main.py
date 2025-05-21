import sys, os
print("DEBUG: sys.path =", sys.path)
print("DEBUG: cwd =", os.getcwd())
print("DEBUG: PYTHONPATH =", os.environ.get("PYTHONPATH"))
# Main entry point for the FastMCP server

from fastmcp import FastMCP
from mcp_server.tools import web_search_tool

class ASGIAppWrapper:
    def __init__(self, fastmcp_instance):
        self.fastmcp = fastmcp_instance
        self._asgi_app = getattr(fastmcp_instance, "app", None)
        if self._asgi_app is None:
            raise RuntimeError("FastMCP instance does not have an internal FastAPI app as 'app' attribute.")

    async def __call__(self, scope, receive, send):
        await self._asgi_app(scope, receive, send)

app = ASGIAppWrapper(
    FastMCP(
        tools=[web_search_tool],
    )
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("mcp_server.main:app", host="0.0.0.0", port=8000, factory=False)