from ollama import chat

from app.schemas.plan import Plan


MODEL = "qwen2.5-coder:7b"


def create_plan(user_request: str) -> Plan:
    response = chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": """
You are an AI agent planner.

Break the user's task into a small number of
clear, actionable steps.

Each step should describe one thing the agent
needs to accomplish.

Do not perform the task.

Return only the plan.
""",
            },
            {
                "role": "user",
                "content": user_request,
            },
        ],
        format=Plan.model_json_schema(),
    )

    return Plan.model_validate_json(
        response.message.content
    )