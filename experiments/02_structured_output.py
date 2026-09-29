from pydantic import BaseModel
from ollama import chat


MODEL = "qwen2.5-coder:7b"


class AgentDecision(BaseModel):
    action: str
    arguments: dict


def main():
    response = chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": """
You are an AI agent.

When given a task, decide what action should be taken.

Return:
- action: the name of the action
- arguments: arguments required for that action

For now, possible actions are:
- calculator
- final_answer
"""
            },
            {
                "role": "user",
                "content": "Calculate 125 multiplied by 48."
            }
        ],
        format=AgentDecision.model_json_schema(),
    )

    print("Raw LLM response:")
    print(response.message.content)

    decision = AgentDecision.model_validate_json(
        response.message.content
    )

    print("\nParsed decision:")
    print(decision)

    print("\nAction:")
    print(decision.action)

    print("\nArguments:")
    print(decision.arguments)


if __name__ == "__main__":
    main()