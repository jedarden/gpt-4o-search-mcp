from fastmcp import FastMCP
from openai import OpenAI
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from typing import Annotated
from pydantic import Field
import os

openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

mcp = FastMCP(
    name="gpt-4o-search",
    instructions="This is a web-accessible search tool that will look up information on the web to answer the question or search query. Call search() to search the web."
)

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> PlainTextResponse:
    return PlainTextResponse("OK")

@mcp.tool()
def search(query: Annotated[str, Field(description="""The search query meant to search on the internet. Can be a question, "What is the address of acme?" Can be an instruction, "Find documentation about this python library." """)]) -> str:
    response = openai_client.chat.completions.create(
        model = "gpt-4o-search-preview",
        messages = [
            {
                "role": "user",
                "content": f"{query}"
            }
        ],
        user = "mcp-gpt-4o-search"
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    mcp.run()