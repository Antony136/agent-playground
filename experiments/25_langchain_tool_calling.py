from langchain_core.tools import tool
from langchain_ollama import ChatOllama


@tool
def calculator(operation: str, numbers: list[float]) -> float:
    """Perform a basic mathematical operation on a list of numbers."""

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

    raise ValueError(
        f"Unsupported operation: {operation}"
    )


llm = ChatOllama(
    model="qwen2.5-coder:7b",
    temperature=0,
)

llm_with_tools = llm.bind_tools([calculator])

response = llm_with_tools.invoke(
    "Calculate 125 multiplied by 48."
)

print("Response:")
print(response)

print("\nTool calls:")
print(response.tool_calls)