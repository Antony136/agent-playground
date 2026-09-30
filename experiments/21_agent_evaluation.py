from app.agent.evaluator import AgentEvaluator
from app.agent.executor import ToolExecutor
from app.agent.loop import AgentLoop
from app.schemas.evaluation import EvaluationCase
from app.tools.default_tools import create_tool_registry


def main():
    registry = create_tool_registry()
    executor = ToolExecutor(registry)
    agent = AgentLoop(executor)

    evaluator = AgentEvaluator(agent)

    cases = [
        EvaluationCase(
            name="simple multiplication",
            request="Calculate 25 multiplied by 4.",
            expected_answer="100",
        ),
        EvaluationCase(
            name="multi-step calculation",
            request="Calculate 20 multiplied by 5, then add 10.",
            expected_answer="110",
        ),
        EvaluationCase(
            name="knowledge base RAG",
            request="According to the knowledge base, what is RAG?",
            expected_answer=(
                "RAG stands for Retrieval-Augmented Generation."
            ),
        ),
    ]

    passed = 0

    print("=" * 60)
    print("AGENT EVALUATION")
    print("=" * 60)

    for case in cases:
        print(f"\nTest: {case.name}")

        result = evaluator.evaluate(case)

        print(f"Expected: {result.expected_answer}")
        print(f"Actual:   {result.actual_answer}")

        if result.passed:
            print("Result:   PASS")
            passed += 1
        else:
            print("Result:   FAIL")

    print("\n" + "=" * 60)
    print(
        f"Passed: {passed}/{len(cases)}"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()