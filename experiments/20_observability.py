from app.agent.executor import ToolExecutor
from app.agent.loop import AgentLoop
from app.agent.observability import AgentTracer
from app.tools.default_tools import create_tool_registry


def main():
    registry = create_tool_registry()
    executor = ToolExecutor(registry)

    tracer = AgentTracer()

    agent = AgentLoop(
        executor=executor,
        tracer=tracer,
    )

    answer = agent.run(
        "Calculate 125 multiplied by 48, then add 250."
    )

    print("\nFinal answer:")
    print(answer)

    print("\nAgent trace:")

    for event in tracer.get_events():
        print(
            f"{event.timestamp} | "
            f"{event.event_type} | "
            f"{event.data}"
        )


if __name__ == "__main__":
    main()