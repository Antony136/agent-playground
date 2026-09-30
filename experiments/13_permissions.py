from app.agent.executor import ToolExecutor
from app.tools.default_tools import create_tool_registry


def main():
    registry = create_tool_registry()
    executor = ToolExecutor(registry)

    print("Calculator:")
    print(
        executor.execute(
            "calculator",
            {
                "operation": "multiply",
                "numbers": [10, 20],
            },
        )
    )

    print("\nRead file:")
    print(
        executor.execute(
            "read_file",
            {
                "file_path": "app/tools/calculator.py",
            },
        )
    )

    print("\nWrite file:")
    print(
        executor.execute(
            "write_file",
            {
                "file_path": "agent_workspace/example.py",
                "content": "print('modified')",
            },
        )
    )

    print("\nUnknown tool:")
    print(
        executor.execute(
            "delete_everything",
            {},
        )
    )


if __name__ == "__main__":
    main()