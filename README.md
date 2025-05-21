# Project Overview

This project is a Python application with support for Docker deployment and MCP (Model Context Protocol) integration for advanced code workflows. The codebase includes the following main files:

- [`app/app.py`](app/app.py): Main application entry point.
- [`requirements.txt`](requirements.txt): Lists Python dependencies required to run the application.
- [`dockerfile`](dockerfile): Instructions for building and running the application in a Docker container.
- [`.env.example`](.env.example): Example environment variables file. Copy this to `.env` and update values as needed.
- [`.roo/mcp.json`](.roo/mcp.json): MCP configuration file for roo code integration.

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

# MCP Configuration Example

To enable roo code integration with the MCP, configure the `.roo/mcp.json` file. Below is a sample configuration and explanation of each field:

```json
{
  "server_url": "http://localhost:5000",
  "api_key": "your-mcp-api-key",
  "project_id": "your-project-id"
}
```

- **server_url**: The URL where your MCP server is running.
- **api_key**: The API key used to authenticate with the MCP server.
- **project_id**: The identifier for your project within the MCP system.

Update these fields in `.roo/mcp.json` to match your MCP deployment.

---

# Example: Using roo code to connect to MCP

Below is an example configuration block for the `gpt-4o-search` MCP service:

```json
"gpt-4o-search": {
  "url": "http://gpt-4o-search-mcp-service.mcp:8000/sse",
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
import requests
import json

# MCP service configuration for gpt-4o-search
mcp_config = {
    "url": "http://link-to-where-service-is-hosted:8000/sse",
    "transport": "http",
    "alwaysAllow": ["search"],
    "timeout": 300
}

def mcp_search(query):
    """
    Connects to the MCP service and performs a 'search' operation.
    Args:
        query (str): The search query string.
    Returns:
        dict: The search results from the MCP service.
    """
    # Prepare the request payload
    payload = {
        "operation": "search",
        "query": query
    }
    # Send the request to the MCP service
    response = requests.post(
        mcp_config["url"],
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"},
        timeout=mcp_config["timeout"]
    )
    response.raise_for_status()
    return response.json()

# Example usage
if __name__ == "__main__":
    result = mcp_search("What is Model Context Protocol?")
    print("Search result:", result)
```

### Explanation

- **mcp_config**: Contains the MCP service connection details as shown in the configuration block.
- **mcp_search(query)**: Defines a function to send a search request to the MCP service. It constructs the payload, sends a POST request, and returns the JSON response.
- **requests.post(...)**: Sends the search operation to the MCP endpoint using the provided configuration.
- **Example usage**: Demonstrates how to call the `mcp_search` function and print the result.

---

# Notes

- Only perform the work outlined above and do not deviate from these instructions.
- For further details, refer to the individual files and comments within the codebase.