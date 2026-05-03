from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from supportops_agent.data_loader import load_collection


class EvalCase(BaseModel):
    id: str = Field(min_length=1)
    input: str = Field(min_length=1)
    expected_tools: list[str] = Field(default_factory=list)
    expected_risk: str = Field(pattern="^(low|medium|high|critical)$")
    must_include_evidence: list[str] = Field(default_factory=list)
    forbidden_actions: list[str] = Field(default_factory=list)
    reference_answer: str = Field(min_length=1)


def load_eval_cases() -> list[EvalCase]:
    return [EvalCase.model_validate(item) for item in load_collection("eval_cases")]


def as_deepeval_rows() -> list[dict[str, Any]]:
    return [case.model_dump() for case in load_eval_cases()]

