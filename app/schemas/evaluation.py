from pydantic import BaseModel


class EvaluationCase(BaseModel):
    name: str
    request: str
    expected_answer: str


class EvaluationResult(BaseModel):
    name: str
    passed: bool
    actual_answer: str
    expected_answer: str