import json
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


@tool
def get_project_info() -> str:
    """Return information about the AI Developer Agent project."""

    return (
        "This is an AI Developer Agent project built with "
        "Python, Ollama, Qwen2.5-Coder, LangGraph and React."
    )


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

Choose the appropriate tool.

Available tools:

1. calculator
Use this for mathematical calculations.

2. get_project_info
Use this when the user asks about this AI Developer Agent project.

If a tool is required, return ONLY JSON:

{{
    "name": "tool_name",
    "arguments": {{}}
}}

For calculator, arguments must look like:

{{
    "operation": "multiply",
    "numbers": [125, 48]
}}

If no tool is required:

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


def route_tool(state: AgentState):
    request = json.loads(state["llm_response"])

    tool_name = request["name"]

    if tool_name == "calculator":
        return "calculator"

    if tool_name == "get_project_info":
        return "get_project_info"

    return "finish"


def execute_calculator(state: AgentState):
    request = json.loads(state["llm_response"])

    result = calculator.invoke(
        request["arguments"]
    )

    print(f"Calculator result: {result}")

    return {
        "tool_result": str(result)
    }


def execute_project_info(state: AgentState):
    result = get_project_info.invoke({})

    print(f"Project info: {result}")

    return {
        "tool_result": result
    }


def finish(state: AgentState):
    if state["tool_result"]:
        response = llm.invoke(
            f"""
The user asked:

{state["user_request"]}

A tool was executed and returned:

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
graph.add_node("calculator", execute_calculator)
graph.add_node("get_project_info", execute_project_info)
graph.add_node("finish", finish)

graph.add_edge(START, "agent")

graph.add_conditional_edges(
    "agent",
    route_tool,
    {
        "calculator": "calculator",
        "get_project_info": "get_project_info",
        "finish": "finish",
    },
)

graph.add_edge("calculator", "finish")
graph.add_edge("get_project_info", "finish")

graph.add_edge("finish", END)

app = graph.compile()


result = app.invoke(
    {
        "user_request": "Tell me about this AI Developer Agent project.",
        "llm_response": "",
        "tool_result": "",
        "final_answer": "",
    }
)

print("\nFinal answer:")
print(result["final_answer"])