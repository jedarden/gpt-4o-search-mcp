# Configuration management for MCP server

import os

def get_settings():
    """
    Loads configuration from environment variables.
    Returns a dict with settings.
    """
    return {
        "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY")
    }