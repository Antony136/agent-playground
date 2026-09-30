from langchain_core.tools import tool
from langchain_ollama import ChatOllama


@tool
def calculator(operation: str, numbers: list[float]) -> float:
    """Perform a basic mathematical operation."""
    if not numbers:
        raise ValueError("At least one number is required.")

    if operation == "add":
        return sum(numbers)

    if operation == "multiply":
        result = 1
        for number in numbers:
            result *= number
        return result

    if operation == "subtract":
        result = numbers[0]
        for number in numbers[1:]:
            result -= number
        return result

    if operation == "divide":
        result = numbers[0]
        for number in numbers[1:]:
            if number == 0:
                raise ValueError("Cannot divide by zero.")
            result /= number

        return result

    raise ValueError(f"Unsupported operation: {operation}")


@tool
def get_project_info() -> str:
    """Return information about the AI agent project."""
    return (
        "This is an AI Developer Agent project built with "
        "Python, Ollama, Qwen2.5-Coder, LangChain and React."
    )


@tool
def get_status() -> str:
    """Return the current project status."""
    return "Project 3 AI Agent is currently being developed."


tools = [
    calculator,
    get_project_info,
    get_status,
]


print("Available LangChain tools:\n")

for tool in tools:
    print(f"Name: {tool.name}")
    print(f"Description: {tool.description}")
    print(f"Schema: {tool.args_schema.model_json_schema()}")
    print()