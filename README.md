# Project Overview

A Model Context Protocol (MCP) server which makes OpenAI's gpt-4o-search-preview model accessible over MCP. 

- [`app/app.py`](app/app.py): Main application entry point.
- [`requirements.txt`](requirements.txt): Lists Python dependencies required to run the application.
- [`dockerfile`](dockerfile): Instructions for building and running the application in a Docker container.
- [`.env.example`](.env.example): Example environment variables file. Copy this to `.env` and update values as needed.

---

# Deployment Instructions

## 1. Environment Variables

Before running the application, set up your environment variables:

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Edit `.env` and update the values as needed for your environment.

## 2. Deploying with Docker

1. Build the Docker image:
   ```bash
   docker build -t my-python-app -f dockerfile .
   ```
2. Run the container:
   ```bash
   docker run --env-file .env -p 8000:8000 my-python-app
   ```

## 3. Deploying with Python (virtualenv)

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set environment variables (see `.env.example`).
4. Run the application:
   ```bash
   python app/app.py
   ```

---

# Example: Using roo code to connect to MCP

Below is an example configuration block for the `gpt-4o-search` MCP service:

```json
"gpt-4o-search": {
  "url": "http://link-to-where-service-is-hosted:8000/sse",
  "transport": "http",
  "alwaysAllow": [
    "search"
  ],
  "timeout": 300
}
```

## Python Example: Performing a "search" Operation

The following Python code demonstrates how to use the above configuration to connect to the MCP service and perform a "search" operation using roo code principles. This example uses the `requests` library to send a search request to the MCP endpoint.
```python
from mcp import MCPClient

# Initialize the MCP client for the gpt-4o-search server
client = MCPClient("http://link-to-where-service-is-hosted:8000/sse")

# Perform a "search" operation
result = client.tool("search", {"query": "What is Model Context Protocol?"})

print("Search result:", result)
### Explanation

- **MCPClient**: The official `mcp` Python library provides the `MCPClient` class to connect to an MCP server.
- **client = MCPClient(...)**: Initializes the client with the URL of the gpt-4o-search MCP server.
- **client.tool("search", {...})**: Performs the "search" operation by specifying the tool name and parameters as a dictionary.
- **Result**: The result of the search operation is printed.

---
# Notes

- Only perform the work outlined above and do not deviate from these instructions.
- For further details, refer to the individual files and comments within the codebase.