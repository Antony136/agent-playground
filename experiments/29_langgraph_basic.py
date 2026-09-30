from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    message: str


def process_message(state: AgentState):
    print("Processing message...")

    return {
        "message": state["message"].upper()
    }


graph = StateGraph(AgentState)

graph.add_node("process", process_message)

graph.add_edge(START, "process")
graph.add_edge("process", END)

app = graph.compile()


result = app.invoke(
    {
        "message": "hello from langgraph"
    }
)

print("\nFinal result:")
print(result)