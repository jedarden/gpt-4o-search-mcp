import sys, os
print("DEBUG: sys.path =", sys.path)
print("DEBUG: cwd =", os.getcwd())
print("DEBUG: PYTHONPATH =", os.environ.get("PYTHONPATH"))
# Main entry point for the FastMCP server

from fastmcp import FastMCP
from mcp_server.tools import web_search_tool

app = FastMCP(
    tools=[web_search_tool],
)