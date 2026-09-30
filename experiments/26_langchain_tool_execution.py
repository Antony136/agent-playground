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

    raise ValueError(f"Unsupported operation: {operation}")


llm = ChatOllama(
    model="qwen2.5-coder:7b",
    temperature=0,
)

llm_with_tools = llm.bind_tools([calculator])

response = llm_with_tools.invoke(
    "Calculate 125 multiplied by 48."
)

print("LLM Response:")
print(response.content)


# Qwen returned the tool call as JSON text.
import json

tool_request = json.loads(response.content)

tool_name = tool_request["name"]
arguments = tool_request["arguments"]

print("\nTool requested:")
print(tool_name)

print("\nArguments:")
print(arguments)


# Execute the requested tool.
if tool_name == "calculator":
    result = calculator.invoke(arguments)
else:
    raise ValueError(f"Unknown tool: {tool_name}")

print("\nTool result:")
print(result)


# Give the tool result back to the LLM.
final_response = llm.invoke(
    f"""
The user asked: Calculate 125 multiplied by 48.

The calculator tool returned this result:
{result}

Give the user the final answer clearly.
"""
)

print("\nFinal answer:")
print(final_response.content)