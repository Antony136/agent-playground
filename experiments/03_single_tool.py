from ollama import chat
from pydantic import BaseModel

from app.tools.calculator import calculator


MODEL = "qwen2.5-coder:7b"


class AgentDecision(BaseModel):
    action: str
    arguments: dict


def ask_llm(user_request: str) -> AgentDecision:
    response = chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": """
You are an AI agent.

Available action:
- calculator

For calculator requests, return:
{
    "action": "calculator",
    "arguments": {
        "operation": "add | subtract | multiply | divide",
        "numbers": [number1, number2, ...]
    }
}
""",
            },
            {
                "role": "user",
                "content": user_request,
            },
        ],
        format=AgentDecision.model_json_schema(),
    )

    return AgentDecision.model_validate_json(
        response.message.content
    )


def main():
    user_request = "Calculate 125 multiplied by 48."

    decision = ask_llm(user_request)

    print("LLM decision:")
    print(decision)

    if decision.action == "calculator":
        result = calculator(
            operation=decision.arguments["operation"],
            numbers=decision.arguments["numbers"],
        )

        print("\nTool result:")
        print(result)


if __name__ == "__main__":
    main()