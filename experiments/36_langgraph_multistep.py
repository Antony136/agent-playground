import json
from typing import TypedDict

from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END

from app.rag_adapter import search_rag


@tool
def search_knowledge_base(query: str) -> str:
    """Search the Project 2 RAG knowledge base."""

    return search_rag(query)


@tool
def calculator(operation: str, numbers: list[float]) -> float:
    """Perform a basic mathematical calculation."""

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
    observations: list[str]
    used_tools: list[str]
    final_answer: str


llm = ChatOllama(
    model="qwen2.5-coder:7b",
    temperature=0,
)


def parse_json_response(response: str) -> dict:
    response = response.strip()

    if response.startswith("```"):
        lines = response.splitlines()

        # Remove opening ```json / ```
        if lines[0].startswith("```"):
            lines = lines[1:]

        # Remove closing ```
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        response = "\n".join(lines).strip()

    return json.loads(response)


def agent(state: AgentState):
    print("\n" + "=" * 60)
    print("AGENT")
    print("=" * 60)

    observations = state["observations"]

    observation_text = "\n\n".join(observations)

    used_tools = state["used_tools"]

    used_tools_text = (
        ", ".join(used_tools)
        if used_tools
        else "None"
    )

    response = llm.invoke(
        f"""
You are an AI research agent.

User request:
{state["user_request"]}

Previous tool observations:
{observation_text if observation_text else "None"}

Tools already completed:
{used_tools_text}

Available tools:

1. search_knowledge_base
Use this to find information from the user's knowledge base.

2. calculator
Use this for mathematical calculations.

Decide what should happen next.

IMPORTANT:
- Never call a tool that is already listed in "Tools already completed".
- If multiple tools are required, use them one at a time.
- If the user needs both RAG and calculator, use
  search_knowledge_base first, then calculator.
- If all required work is complete, return "none".

For RAG:

{{
    "name": "search_knowledge_base",
    "arguments": {{
        "query": "the user's relevant question"
    }}
}}

For calculator:

{{
    "name": "calculator",
    "arguments": {{
        "operation": "multiply",
        "numbers": [125, 48]
    }}
}}

If all required work is complete:

{{
    "name": "none",
    "arguments": {{}}
}}

Return ONLY JSON.
"""
    )

    print("LLM decision:")
    print(response.content)

    return {
        "llm_response": response.content
    }


def route_agent(state: AgentState):
    decision = parse_json_response(state["llm_response"])

    if decision["name"] == "search_knowledge_base":
        return "search_knowledge_base"

    if decision["name"] == "calculator":
        return "calculator"

    return "finish"


def execute_rag(state: AgentState):
    decision = parse_json_response(state["llm_response"])

    result = search_knowledge_base.invoke(
        decision["arguments"]
    )

    print("\nRAG completed.")

    return {
        "tool_result": result,
        "observations": state["observations"] + [
            f"RAG observation:\n{result}"
        ],
        "used_tools": state["used_tools"] + [
            "search_knowledge_base"
        ],
    }


def execute_calculator(state: AgentState):
    decision = parse_json_response(state["llm_response"])

    result = calculator.invoke(
        decision["arguments"]
    )

    print(f"\nCalculator result: {result}")

    return {
        "tool_result": str(result),
        "observations": state["observations"] + [
            f"Calculator observation: {result}"
        ],
        "used_tools": state["used_tools"] + [
            "calculator"
        ],
    }


def finish(state: AgentState):
    print("\n" + "=" * 60)
    print("FINISH")
    print("=" * 60)

    observations = "\n\n".join(state["observations"])

    response = llm.invoke(
        f"""
Answer the user's original request using the observations below.

User request:
{state["user_request"]}

Observations:
{observations}

Give one clear answer covering everything the user asked.

Do not invent information that is not present in the observations.
"""
    )

    return {
        "final_answer": response.content
    }


graph = StateGraph(AgentState)

graph.add_node("agent", agent)
graph.add_node("search_knowledge_base", execute_rag)
graph.add_node("calculator", execute_calculator)
graph.add_node("finish", finish)

graph.add_edge(START, "agent")

graph.add_conditional_edges(
    "agent",
    route_agent,
    {
        "search_knowledge_base": "search_knowledge_base",
        "calculator": "calculator",
        "finish": "finish",
    },
)

# After each tool, return to the agent.
graph.add_edge("search_knowledge_base", "agent")
graph.add_edge("calculator", "agent")

graph.add_edge("finish", END)

app = graph.compile()


result = app.invoke(
    {
        "user_request": (
            "According to my knowledge base, explain what RAG is, "
            "and calculate 125 multiplied by 48."
        ),
        "llm_response": "",
        "tool_result": "",
        "observations": [],
        "used_tools": [],
        "final_answer": "",
    }
)


print("\n" + "=" * 60)
print("FINAL ANSWER")
print("=" * 60)
print(result["final_answer"])