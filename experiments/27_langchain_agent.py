from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langchain.agents import create_agent


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

agent = create_agent(
    model=llm,
    tools=[calculator],
    system_prompt="You are a helpful assistant. Use the calculator tool when mathematical calculation is required.",
)

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Calculate 125 multiplied by 48."
            }
        ]
    }
)

for message in result["messages"]:
    print(f"\n{message.__class__.__name__}:")
    print(message.content)