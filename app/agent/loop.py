from ollama import chat
from pydantic import BaseModel

from app.agent.executor import ToolExecutor
from app.agent.state import AgentState


MODEL = "qwen2.5-coder:7b"


class AgentDecision(BaseModel):
    action: str
    arguments: dict


class AgentLoop:
    def __init__(self, executor: ToolExecutor):
        self.executor = executor

    def ask_llm(self, messages: list[dict]) -> AgentDecision:
        response = chat(
            model=MODEL,
            messages=messages,
            format=AgentDecision.model_json_schema(),
        )

        return AgentDecision.model_validate_json(
            response.message.content
        )

    def run(self, user_request: str) -> str:
        state = AgentState(
            user_request=user_request,
            messages=[
                {
                    "role": "system",
                    "content": """
You are an AI developer agent.

You have access to these actions:

calculator
- Perform arithmetic calculations.

list_files
- List files inside a directory.

read_file
- Read the contents of a text file.

search_files
- Search files recursively for text.

get_exchange_rate
- Get the exchange rate between two currencies.

search_knowledge_base
- Search the knowledge base for relevant information.

final_answer
- Use this when the user's task is complete.

For calculator requests, return:

{
    "action": "calculator",
    "arguments": {
        "operation": "add | subtract | multiply | divide",
        "numbers": [number1, number2, ...]
    }
}

For list_files:

{
    "action": "list_files",
    "arguments": {
        "directory": "directory path"
    }
}

For read_file:

{
    "action": "read_file",
    "arguments": {
        "file_path": "file path"
    }
}

For search_files:

{
    "action": "search_files",
    "arguments": {
        "directory": "directory path",
        "query": "text to search for"
    }
}

For get_exchange_rate:

{
    "action": "get_exchange_rate",
    "arguments": {
        "base_currency": "USD",
        "target_currency": "EUR"
    }
}

For search_knowledge_base:

{
    "action": "search_knowledge_base",
    "arguments": {
        "query": "your search query"
    }
}

When the task is complete, return:

{
    "action": "final_answer",
    "arguments": {
        "answer": "your final answer"
    }
}

You may perform multiple tool calls.

Use results from previous tool calls when necessary.

Return only the structured response.
""",
                },
                {
                    "role": "user",
                    "content": user_request,
                },
            ],
        )

        while True:
            state.iteration += 1

            decision = self.ask_llm(state.messages)

            state.current_action = decision.action

            print("\nAgent state:")
            print(f"Iteration: {state.iteration}")
            print(f"Current action: {state.current_action}")

            print("\nAgent decision:")
            print(decision)

            if decision.action == "final_answer":
                return decision.arguments["answer"]

            result = self.executor.execute(
                tool_name=decision.action,
                arguments=decision.arguments,
            )

            print("\nTool result:")
            print(result)

            if not result.success:
                return f"Tool execution failed: {result.error}"

            state.tool_results.append(str(result.result))

            state.messages.append(
                {
                    "role": "assistant",
                    "content": decision.model_dump_json(),
                }
            )

            state.messages.append(
                {
                    "role": "user",
                    "content": f"""
The tool `{decision.action}` returned:

{result.result}

Use this result to continue the task.

If another tool is needed, call it.

If the task is complete, return final_answer.
""",
                }
            )