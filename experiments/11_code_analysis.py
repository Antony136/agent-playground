from app.agent.executor import ToolExecutor
from app.agent.loop import AgentLoop
from app.tools.default_tools import create_tool_registry


def main():
    registry = create_tool_registry()
    executor = ToolExecutor(registry)

    agent = AgentLoop(executor)

    answer = agent.run(
        """
Analyze the file app/tools/calculator.py.

Explain:
1. What the file does
2. What functions it contains
3. What parameters the functions accept
4. What operations are supported
5. Any obvious potential issues
"""
    )

    print("\nFinal answer:")
    print(answer)


if __name__ == "__main__":
    main()