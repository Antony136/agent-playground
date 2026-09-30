import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.server.mcpserver import MCPServer


server = MCPServer("AI Agent Resources")


@server.resource("project://info")
def project_info() -> str:
    return """
AI Developer Agent

Project 3 of the AI learning roadmap.

Technologies:
- Python
- Ollama
- Qwen 2.5 Coder
- LangChain
- LangGraph
- MCP
- FastAPI
- React
"""


async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "experiments.39_mcp_resources"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            resources = await session.list_resources()

            print("\nAvailable MCP resources:")

            for resource in resources.resources:
                print(f"- {resource.uri}")

            result = await session.read_resource("project://info")

            print("\nResource content:")

            for content in result.contents:
                print(content.text)


if __name__ == "__main__":
    asyncio.run(main())