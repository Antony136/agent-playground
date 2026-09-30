import json
from typing import TypedDict

from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END

from app.rag_adapter import search_rag


@tool
def search_knowledge_base(query: str) -> str:
    """Search the Project 2 RAG knowledge base for relevant information."""

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
    final_answer: str


llm = ChatOllama(
    model="qwen2.5-coder:7b",
    temperature=0,
)


def agent(state: AgentState):
    print("\nLLM thinking...")

    response = llm.invoke(
        f"""
You are an AI research agent.

User request:
{state["user_request"]}

Choose the appropriate tool.

Available tools:

1. calculator
Use for mathematical calculations.

2. search_knowledge_base
Use when the user asks about information that may exist
inside the knowledge base.

For search_knowledge_base, pass the user's complete question
or a meaningful natural-language query.

If a tool is required, return ONLY JSON.

Calculator example:

{{
    "name": "calculator",
    "arguments": {{
        "operation": "multiply",
        "numbers": [125, 48]
    }}
}}

Knowledge-base example:

{{
    "name": "search_knowledge_base",
    "arguments": {{
        "query": "What is Retrieval-Augmented Generation?"
    }}
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

    if request["name"] == "calculator":
        return "calculator"

    if request["name"] == "search_knowledge_base":
        return "search_knowledge_base"

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


def execute_rag(state: AgentState):
    request = json.loads(state["llm_response"])

    result = search_knowledge_base.invoke(
        request["arguments"]
    )

    print("\nRAG result:")
    print(result)

    return {
        "tool_result": result
    }


def finish(state: AgentState):
    if not state["tool_result"]:
        return {
            "final_answer": state["llm_response"]
        }

    response = llm.invoke(
        f"""
Answer the user's question using the tool result below.

User question:
{state["user_request"]}

Tool result:
{state["tool_result"]}

Give a clear, concise answer.
Do not invent information that is not present in the tool result.
"""
    )

    return {
        "final_answer": response.content
    }


graph = StateGraph(AgentState)

graph.add_node("agent", agent)
graph.add_node("calculator", execute_calculator)
graph.add_node("search_knowledge_base", execute_rag)
graph.add_node("finish", finish)

graph.add_edge(START, "agent")

graph.add_conditional_edges(
    "agent",
    route_tool,
    {
        "calculator": "calculator",
        "search_knowledge_base": "search_knowledge_base",
        "finish": "finish",
    },
)

graph.add_edge("calculator", "finish")
graph.add_edge("search_knowledge_base", "finish")
graph.add_edge("finish", END)

app = graph.compile()


result = app.invoke(
    {
        "user_request": "According to my knowledge base, what is RAG?",
        "llm_response": "",
        "tool_result": "",
        "final_answer": "",
    }
)

print("\nFinal answer:")
print(result["final_answer"])