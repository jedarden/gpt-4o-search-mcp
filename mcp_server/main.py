# Main entry point for the FastMCP server

from fastmcp import FastMCP
from mcp_server.tools import web_search_tool

app = FastMCP(
    tools=[web_search_tool],
)