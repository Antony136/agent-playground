from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    user_request: str
    decision: str
    tool_result: str
    final_answer: str


def agent(state: AgentState):
    if state["tool_result"]:
        print("\nLLM received tool result.")

        return {
            "decision": "none",
            "final_answer": (
                f"The calculation result is {state['tool_result']}."
            )
        }

    request = state["user_request"].lower()

    print("\nLLM thinking...")

    if "calculate" in request or "multiply" in request:
        print("LLM decided: calculator")

        return {
            "decision": "calculator"
        }

    print("LLM decided: final answer")

    return {
        "decision": "none",
        "final_answer": "I can answer this without using a tool."
    }


def execute_tool(state: AgentState):
    print("Executing calculator...")

    # Simulate calculator result.
    result = "6000"

    return {
        "tool_result": result
    }


def route_after_agent(state: AgentState):
    if state["decision"] == "calculator":
        return "execute_tool"

    return "finish"


def finish(state: AgentState):
    if state["tool_result"]:
        return {
            "final_answer": (
                f"The calculation result is {state['tool_result']}."
            )
        }

    return {
        "final_answer": state["final_answer"]
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

# The important loop:
graph.add_edge("execute_tool", "agent")

graph.add_edge("finish", END)

app = graph.compile()


result = app.invoke(
    {
        "user_request": "Calculate 125 multiplied by 48.",
        "decision": "",
        "tool_result": "",
        "final_answer": "",
    }
)

print("\nFinal answer:")
print(result["final_answer"])