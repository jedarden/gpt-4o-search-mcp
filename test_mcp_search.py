from mcp import MCPClient

# Initialize the MCP client for the gpt-4o-search server
client = MCPClient("http://localhost:8000/sse")

# Perform a "search" operation
result = client.tool("search", {"query": "What is Model Context Protocol?"})

print("Search result:", result)