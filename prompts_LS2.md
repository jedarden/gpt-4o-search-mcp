## Prompt [LS2_1]

### Context
The core web search tool and OpenAI integration are currently stubs in [`mcp_server/tools.py`](mcp_server/tools.py:8) and [`mcp_server/openai_client.py`](mcp_server/openai_client.py:3). The server cannot fulfill its intended purpose. No actual API calls or result handling are implemented.

### Objective
Implement the core web search tool and OpenAI API integration so that the server can process queries and return real search results.

### Focus Areas
- Implement `web_search_tool` to call the OpenAI API using the gpt-4o-search-preview model.
- Implement `search_openai` to perform the actual HTTP request to OpenAI.
- Handle API keys securely via configuration.
- Add input validation and error handling.

### Code Reference
```python
# mcp_server/tools.py
def web_search_tool(query: str):
    """
    Web search tool that calls OpenAI API with the gpt-4o-search-preview model.
    """
    # Implementation will be added
    pass
```

### Requirements
- Use async HTTP client (e.g., httpx) for OpenAI API calls.
- Validate and sanitize all user input.
- Do not log or expose API keys.
- Return structured results or error messages.

### Expected Improvements
- Correctness: +60 (logic, edge case handling)
- Performance: +40 (async, efficient API usage)
- Security: +40 (input validation, secret handling)


---

## Prompt [LS2_2]

### Context
All test functions in [`tests/test_web_search.py`](tests/test_web_search.py:17) are stubs. There is no automated verification of functionality, correctness, or error handling. Coverage is 0%.

### Objective
Add real, passing tests for all implemented features and edge cases using pytest and httpx.AsyncClient.

### Focus Areas
- Implement tests for valid and invalid queries.
- Test error handling and edge cases.
- Ensure tests cover all endpoints and major code paths.

### Code Reference
```python
def test_valid_search_query():
    """Arrange: Valid query. Act: Call endpoint. Assert: Results returned."""
    pass
```

### Requirements
- Use pytest and httpx.AsyncClient for FastAPI endpoints.
- Achieve at least 80% line and branch coverage.
- Include both positive and negative test cases.

### Expected Improvements
- Coverage: +80
- Correctness: +40 (edge case handling)
- Security: +20 (input validation tested)


---

## Prompt [LS2_3]

### Context
Dependencies in [`requirements.txt`](requirements.txt:1) are not version-pinned, risking reproducibility and security.

### Objective
Pin all dependencies in requirements.txt to specific, tested versions.

### Focus Areas
- Specify exact versions for all packages.
- Research and use secure, compatible versions.

### Code Reference
```
fastapi
uvicorn
httpx
pytest
python-dotenv
```

### Requirements
- Replace each dependency with `package==version`.
- Ensure all versions are compatible and up-to-date.
- Document any version constraints in README.

### Expected Improvements
- Security: +40 (supply chain)
- Correctness: +10 (reproducibility)


---

## Prompt [LS2_4]

### Context
The [`Dockerfile`](Dockerfile:3) installs unnecessary packages, runs as root, and does not handle secrets securely. Security and performance scores are low.

### Objective
Refactor the Dockerfile for security and best practices.

### Focus Areas
- Remove unnecessary packages (e.g., build-essential if not compiling).
- Add a non-root user and switch to it.
- Use multi-stage builds if appropriate.
- Document and secure .env usage.

### Code Reference
```dockerfile
FROM python:3.11-slim
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*
```

### Requirements
- Only install required system packages.
- Ensure the container does not run as root.
- Do not bake secrets into the image.
- Add comments explaining security measures.

### Expected Improvements
- Security: +60
- Performance: +20
- Correctness: +10


---

## Prompt [LS2_5]

### Context
The [`README.md`](README.md:10,12,55) claims features (input validation, error handling, endpoint, tests) that are not present in the codebase.

### Objective
Ensure documentation matches the actual codebase and does not overstate features.

### Focus Areas
- Update README to reflect current and implemented features.
- Add or remove sections as needed for accuracy.
- Document usage, configuration, and limitations.

### Code Reference
```
- Input validation and robust error handling
- Unit tests and CI-ready
- Web search tool endpoint
```

### Requirements
- Remove or revise claims about unimplemented features.
- Add setup and usage instructions for new features.
- Document environment variables and security practices.

### Expected Improvements
- Correctness: +20 (documentation accuracy)
- Security: +10 (documented practices)
- Coverage: +10 (test documentation)