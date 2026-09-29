from app.tools.default_tools import create_tool_registry


def main():
    registry = create_tool_registry()

    print("Available tools:\n")

    for tool in registry.list_tools():
        print(f"- {tool.name}")
        print(f"  {tool.schema.description}")


if __name__ == "__main__":
    main()