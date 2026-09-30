from app.agent.executor import ToolExecutor
from app.agent.loop import AgentLoop
from app.tools.default_tools import create_tool_registry


def main():
    registry = create_tool_registry()
    executor = ToolExecutor(registry)

    agent = AgentLoop(executor)

    answer = agent.run(
        "What is the current exchange rate from USD to EUR?"
    )

    print("\nFinal answer:")
    print(answer)


if __name__ == "__main__":
    main()