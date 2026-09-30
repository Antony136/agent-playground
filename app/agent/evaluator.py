from app.agent.loop import AgentLoop
from app.schemas.evaluation import (
    EvaluationCase,
    EvaluationResult,
)


class AgentEvaluator:
    def __init__(self, agent: AgentLoop):
        self.agent = agent

    def evaluate(
        self,
        case: EvaluationCase,
    ) -> EvaluationResult:

        actual_answer = self.agent.run(case.request)

        passed = str(actual_answer).strip().lower() == (
            case.expected_answer.strip().lower()
        )

        return EvaluationResult(
            name=case.name,
            passed=passed,
            actual_answer=str(actual_answer),
            expected_answer=case.expected_answer,
        )