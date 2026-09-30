from typing import TypedDict

from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END


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


class AgentState(TypedDict):
    user_request: str
    llm_response: str
    tool_result: str
    final_answer: str


llm = ChatOllama(
    model="qwen2.5-coder:7b",
    temperature=0,
)


def agent(state: AgentState):
    print("\nLLM thinking...")

    response = llm.invoke(
        f"""
You are an AI agent.

User request:
{state["user_request"]}

If the request requires a calculation, return ONLY a JSON object
in this format:

{{
    "name": "calculator",
    "arguments": {{
        "operation": "multiply",
        "numbers": [125, 48]
    }}
}}

If no tool is required, return:

{{
    "name": "none",
    "arguments": {{}}
}}

Do not include any other text.
"""
    )

    print("LLM response:")
    print(response.content)

    return {
        "llm_response": response.content
    }


def execute_tool(state: AgentState):
    import json

    request = json.loads(state["llm_response"])

    if request["name"] == "calculator":
        result = calculator.invoke(
            request["arguments"]
        )

        print(f"Tool result: {result}")

        return {
            "tool_result": str(result)
        }

    return {
        "tool_result": ""
    }


def route_after_agent(state: AgentState):
    import json

    request = json.loads(state["llm_response"])

    if request["name"] == "calculator":
        return "execute_tool"

    return "finish"


def finish(state: AgentState):
    if state["tool_result"]:
        response = llm.invoke(
            f"""
The user asked:

{state["user_request"]}

The calculator returned:

{state["tool_result"]}

Give the user a clear final answer.
"""
        )

        return {
            "final_answer": response.content
        }

    return {
        "final_answer": state["llm_response"]
    }


graph = StateGraph(AgentState)

graph.add_node("agent", agent)
graph.add_node("execute_tool", execute_tool)
graph.add_node("finish", finish)

graph.add_edge(START, "agent")

graph.add_conditional_edges(
    "agent",
    route_after_agent,
    {
        "execute_tool": "execute_tool",
        "finish": "finish",
    },
)

graph.add_edge("execute_tool", "finish")
graph.add_edge("finish", END)

app = graph.compile()


result = app.invoke(
    {
        "user_request": "Calculate 125 multiplied by 48.",
        "llm_response": "",
        "tool_result": "",
        "final_answer": "",
    }
)

print("\nFinal answer:")
print(result["final_answer"])