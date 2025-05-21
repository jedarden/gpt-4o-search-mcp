# Dockerfile for FastMCP Web Search MCP Server
# Deployment best practices: see https://gofastmcp.com/servers/fastmcp
# - Use minimal base image
# - Run as non-root user
# - Do NOT bake secrets into the image; mount .env at runtime
# - Use `fastmcp serve` as the entrypoint (not uvicorn)
# - Expose only required ports
# - For more, see official FastMCP docs above

FROM python:3.11-slim

# Set work directory
WORKDIR /app

# OCI label for GitHub source repository (see https://github.com/opencontainers/image-spec/blob/main/annotations.md)
LABEL org.opencontainers.image.source="https://github.com/${GITHUB_REPOSITORY}"

# Install only required system dependencies (none needed for pure Python)
# If you need to install OS packages, add them here.

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create a non-root user and switch to it for security
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Expose port (default FastMCP/FastAPI port)
EXPOSE 8000

# Set environment variables (use .env at runtime, do NOT bake secrets into the image)
ENV PYTHONUNBUFFERED=1

# Security: .env file should be mounted at runtime, not copied into the image.
# Example: docker run --env-file .env ...

# Start the FastMCP server using the official CLI
CMD ["fastmcp", "run", "mcp_server/main.py:mcp", "--transport", "streamable-http"]