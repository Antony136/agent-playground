from app.agent.executor import ToolExecutor
from app.agent.loop import AgentLoop
from app.tools.default_tools import create_tool_registry


def main():
    registry = create_tool_registry()
    executor = ToolExecutor(registry)

    agent = AgentLoop(executor)

    answer = agent.run(
        """
Research the files inside app/tools.

First find the files in that directory.
Then search those files for the word "calculator".
Finally, explain which files contain that word.
"""
    )

    print("\nFinal answer:")
    print(answer)


if __name__ == "__main__":
    main()