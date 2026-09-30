from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    user_request: str
    decision: str
    tool_result: str


def decide(state: AgentState):
    request = state["user_request"]

    print(f"Agent received: {request}")

    return {
        "decision": "calculator"
    }


def execute_tool(state: AgentState):
    decision = state["decision"]

    print(f"Executing tool: {decision}")

    return {
        "tool_result": "6000"
    }


def final_answer(state: AgentState):
    result = state["tool_result"]

    print(f"Tool result: {result}")

    return {
        "tool_result": result
    }


graph = StateGraph(AgentState)

graph.add_node("decide", decide)
graph.add_node("execute_tool", execute_tool)
graph.add_node("final_answer", final_answer)

graph.add_edge(START, "decide")
graph.add_edge("decide", "execute_tool")
graph.add_edge("execute_tool", "final_answer")
graph.add_edge("final_answer", END)

app = graph.compile()


result = app.invoke(
    {
        "user_request": "Calculate 125 multiplied by 48.",
        "decision": "",
        "tool_result": "",
    }
)

print("\nFinal state:")
print(result)