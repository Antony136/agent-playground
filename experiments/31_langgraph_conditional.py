from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    user_request: str
    decision: str
    tool_result: str


def decide(state: AgentState):
    request = state["user_request"].lower()

    print(f"Agent received: {state['user_request']}")

    if "calculate" in request or "multiply" in request:
        return {
            "decision": "calculator"
        }

    return {
        "decision": "none"
    }


def execute_tool(state: AgentState):
    print("Executing calculator...")

    return {
        "tool_result": "6000"
    }


def route_after_decision(state: AgentState):
    if state["decision"] == "calculator":
        return "execute_tool"

    return END


graph = StateGraph(AgentState)

graph.add_node("decide", decide)
graph.add_node("execute_tool", execute_tool)

graph.add_edge(START, "decide")

graph.add_conditional_edges(
    "decide",
    route_after_decision,
    {
        "execute_tool": "execute_tool",
        END: END,
    },
)

graph.add_edge("execute_tool", END)

app = graph.compile()


result = app.invoke(
    {
        "user_request": "What is an AI agent?",
        "decision": "",
        "tool_result": "",
    }
)

print("\nFinal state:")
print(result)