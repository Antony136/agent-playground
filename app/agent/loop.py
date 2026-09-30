from ollama import chat
from pydantic import BaseModel

from app.agent.executor import ToolExecutor
from app.agent.state import AgentState
from app.agent.observability import AgentTracer


MODEL = "qwen2.5-coder:7b"


class AgentDecision(BaseModel):
    action: str
    arguments: dict


class AgentLoop:
    def __init__(
        self,
        executor: ToolExecutor,
        tracer: AgentTracer | None = None,
    ):
        self.executor = executor
        self.tracer = tracer or AgentTracer()

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
You are an AI agent.

You can use these actions:

calculator
- Perform arithmetic calculations.

list_files
- List files inside a directory.

read_file
- Read a text file.

search_files
- Search files recursively for text.

write_file
- Write or modify a file inside the allowed agent workspace.
- This action requires permission/approval.

get_exchange_rate
- Get the exchange rate between two currencies.

search_knowledge_base
- Search the knowledge base for relevant information.
- For search_knowledge_base, pass the user's full question or a meaningful natural-language query.
- Do not reduce the user's question to a single keyword.
- The knowledge-base search system performs its own query normalization, rewriting, retrieval, and reranking.
- Use the retrieved information as evidence when producing the final answer.

final_answer
- Return the final answer when the task is complete.

If a tool returns an error:
- Analyze the error.
- If possible, correct the arguments and retry.
- If another tool can solve the problem, use it.
- If the problem cannot be solved, return a final answer explaining the issue.

For calculator:

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
        "directory": "path"
    }
}

For read_file:

{
    "action": "read_file",
    "arguments": {
        "file_path": "path"
    }
}

For search_files:

{
    "action": "search_files",
    "arguments": {
        "directory": "path",
        "query": "text"
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

When the task is complete:

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
            ],
        )

        self.tracer.record(
            "agent_started",
            {
                "user_request": user_request,
            },
        )

        max_iterations = 10

        while state.iteration < max_iterations:
            state.iteration += 1

            decision = self.ask_llm(state.messages)
            state.current_action = decision.action

            print("\nAgent state:")
            print(f"Iteration: {state.iteration}")
            print(f"Current action: {state.current_action}")

            print("\nAgent decision:")
            print(decision)

            self.tracer.record(
                "llm_decision",
                {
                    "iteration": state.iteration,
                    "action": decision.action,
                    "arguments": decision.arguments,
                },
            )

            if decision.action == "final_answer":
                answer = decision.arguments["answer"]

                self.tracer.record(
                    "agent_completed",
                    {
                        "answer": answer,
                        "iterations": state.iteration,
                    },
                )

                return answer

            self.tracer.record(
                "tool_started",
                {
                    "tool": decision.action,
                    "arguments": decision.arguments,
                    "iteration": state.iteration,
                },
            )

            result = self.executor.execute(
                tool_name=decision.action,
                arguments=decision.arguments,
            )

            print("\nTool result:")
            print(result)

            state.messages.append(
                {
                    "role": "assistant",
                    "content": decision.model_dump_json(),
                }
            )

            if result.success:
                self.tracer.record(
                    "tool_completed",
                    {
                        "tool": decision.action,
                        "result": str(result.result),
                        "iteration": state.iteration,
                    },
                )

                state.tool_results.append(str(result.result))

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

            else:
                self.tracer.record(
                    "tool_failed",
                    {
                        "tool": decision.action,
                        "error": result.error,
                        "iteration": state.iteration,
                    },
                )

                state.messages.append(
                    {
                        "role": "user",
                        "content": f"""
The tool `{decision.action}` failed.

Error:
{result.error}

Analyze this error carefully.

If you can fix the problem, retry with corrected arguments.
If another tool can solve the problem, use that tool.
If the task cannot be completed, return final_answer explaining why.
""",
                    }
                )

        self.tracer.record(
            "agent_stopped",
            {
                "reason": "maximum_iterations_reached",
                "iterations": state.iteration,
            },
        )

        return "The agent stopped because it reached the maximum number of iterations."
