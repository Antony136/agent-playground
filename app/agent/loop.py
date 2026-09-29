from ollama import chat
from pydantic import BaseModel

from app.agent.executor import ToolExecutor


MODEL = "qwen2.5-coder:7b"


class AgentDecision(BaseModel):
    action: str
    arguments: dict


class AgentLoop:
    def __init__(self, executor: ToolExecutor):
        self.executor = executor

    def ask_llm(
        self,
        user_request: str,
        tool_result: str | None = None,
    ) -> AgentDecision:

        messages = [
            {
                "role": "system",
                "content": """
You are an AI agent.

You have access to these actions:

1. calculator
   Use this for arithmetic calculations.

2. final_answer
   Use this when you can provide the final answer to the user.

For calculator requests, return:

{
    "action": "calculator",
    "arguments": {
        "operation": "add | subtract | multiply | divide",
        "numbers": [number1, number2, ...]
    }
}

When you have enough information to answer the user, return:

{
    "action": "final_answer",
    "arguments": {
        "answer": "your final answer"
    }
}

Return only the structured response.
""",
            },
            {
                "role": "user",
                "content": user_request,
            },
        ]

        if tool_result is not None:
            messages.append(
                {
                    "role": "user",
                    "content": f"""
The tool returned this result:

{tool_result}

Now decide what to do next.
If the task is complete, return final_answer.
""",
                }
            )

        response = chat(
            model=MODEL,
            messages=messages,
            format=AgentDecision.model_json_schema(),
        )

        return AgentDecision.model_validate_json(
            response.message.content
        )

    def run(self, user_request: str) -> str:

        tool_result = None

        while True:

            decision = self.ask_llm(
                user_request=user_request,
                tool_result=tool_result,
            )

            print("\nAgent decision:")
            print(decision)

            if decision.action == "final_answer":
                return decision.arguments["answer"]

            tool_result = self.executor.execute(
                tool_name=decision.action,
                arguments=decision.arguments,
            )

            print("\nTool result:")
            print(tool_result)

            if not tool_result.success:
                return f"Tool execution failed: {tool_result.error}"

            tool_result = str(tool_result.result)