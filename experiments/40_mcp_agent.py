import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "experiments.37_mcp_server"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 1. Connect to MCP server
            await session.initialize()

            # 2. Discover available tools
            tools = await session.list_tools()

            print("Available MCP tools:")

            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")

            # 3. Simulate the agent deciding to use calculator
            print("\nAgent decision:")
            print("Use calculator with 125 × 48")

            # 4. Ask MCP server to execute the tool
            result = await session.call_tool(
                "calculator",
                {
                    "operation": "multiply",
                    "numbers": [125, 48],
                },
            )

            # 5. Give the result back to the agent
            print("\nObservation:")

            for content in result.content:
                print(content.text)

            print("\nAgent final answer:")
            print("125 × 48 = 6000")


if __name__ == "__main__":
    asyncio.run(main())