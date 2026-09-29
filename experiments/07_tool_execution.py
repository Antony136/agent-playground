from app.agent.executor import ToolExecutor
from app.tools.default_tools import create_tool_registry


def main():
    registry = create_tool_registry()
    executor = ToolExecutor(registry)

    result = executor.execute(
        tool_name="list_files",
        arguments={
            "directory": "app/tools",
        },
    )

    print("Execution result:")
    print(result)

    print("\nSuccess:")
    print(result.success)

    print("\nResult:")
    print(result.result)

    print("\nError:")
    print(result.error)


if __name__ == "__main__":
    main()