## Prompt LS1_1

### Context
You are to implement an MCP server using FastMCP that exposes a web search tool. The tool should accept a search query, call the OpenAI API using the gpt-4o-search-preview model, and return search results to the client. The server must securely handle the OpenAI API key via environment variables and follow modular, secure, and best-practice code organization.

### Task
Implement the core FastMCP server with a web search tool endpoint.

### Requirements
- Use FastMCP to create the MCP server.
- Expose a tool endpoint that accepts a search query as input.
- Integrate with the OpenAI API, using the gpt-4o-search-preview model.
- Return search results in a structured JSON format.
- Organize code into clear, modular components (e.g., server, tool, OpenAI integration).
- Follow security and code quality best practices.

### Previous Issues
N/A (first iteration)

### Expected Output
- Source code files for the FastMCP server and web search tool.
- Modular structure (separate files/modules for server, tool, and OpenAI integration).
- Inline comments explaining key logic and security considerations.

---

## Prompt LS1_2

### Context
The MCP server must securely store and access the OpenAI API key, never exposing it to the client or in source code. The key should be loaded from an environment variable.

### Task
Implement secure API key management for the OpenAI integration.

### Requirements
- Load the OpenAI API key from an environment variable (e.g., OPENAI_API_KEY).
- Do not hardcode the API key in any source file.
- Ensure the key is never sent to the client or logged.
- Provide an example environment file (.env.example) with placeholder values.
- Add documentation/comments on secure key handling.

### Previous Issues
N/A

### Expected Output
- Secure API key loading logic in the OpenAI integration module.
- .env.example file with placeholder for OPENAI_API_KEY.
- Documentation/comments on secure practices.

---

## Prompt LS1_3

### Context
The web search tool must validate input and handle errors gracefully, providing clear feedback to the client and avoiding information leakage.

### Task
Implement input validation and robust error handling for the web search tool endpoint.

### Requirements
- Validate that the search query is present, non-empty, and a string.
- Return appropriate error responses for invalid input (e.g., 400 Bad Request).
- Catch and handle errors from the OpenAI API call, returning a generic error message to the client (e.g., 502 Bad Gateway).
- Log errors server-side without exposing sensitive details to the client.
- Include tests for input validation and error scenarios.

### Previous Issues
N/A

### Expected Output
- Input validation logic in the tool endpoint.
- Error handling code for both input and OpenAI API failures.
- Test cases covering valid, invalid, and edge-case inputs.

---

## Prompt LS1_4

### Context
The MCP server must be easily deployable using Docker, with all necessary configuration for environment variables and dependencies.

### Task
Create Docker deployment configuration for the FastMCP server.

### Requirements
- Write a Dockerfile that builds and runs the server.
- Use multi-stage builds if appropriate for security and efficiency.
- Ensure environment variables (e.g., OPENAI_API_KEY) are configurable at runtime.
- Provide a docker-compose.yml if multiple services or easier local development is needed.
- Document build and run instructions in a README section or comments.

### Previous Issues
N/A

### Expected Output
- Dockerfile (and docker-compose.yml if needed).
- Documentation for Docker-based deployment and configuration.

---

## Prompt LS1_5

### Context
The project must be test-driven, with clear specifications for expected behaviors and edge cases. Tests should be written before implementation and cover all critical paths.

### Task
Define TDD-ready test specifications for the MCP server and web search tool.

### Requirements
- Specify test cases for:
  - Valid search queries (typical, long, special characters).
  - Missing or invalid queries (empty, non-string).
  - OpenAI API errors (network failure, invalid API key, rate limiting).
  - Security (API key never exposed).
- Use Arrange-Act-Assert pattern in test descriptions.
- Include edge cases and negative scenarios.
- Structure tests for independence and clarity.

### Previous Issues
N/A

### Expected Output
- Test specification file (e.g., tests/test_web_search.py or similar).
- Well-documented test cases ready for TDD implementation.