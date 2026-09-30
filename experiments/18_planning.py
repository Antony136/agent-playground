from app.agent.planner import create_plan


def main():
    plan = create_plan(
        """
Research what RAG is using the knowledge base,
then calculate 125 multiplied by 48,
and combine both results into one answer.
"""
    )

    print("Generated plan:")

    for index, step in enumerate(plan.steps, start=1):
        print(f"{index}. {step}")


if __name__ == "__main__":
    main()