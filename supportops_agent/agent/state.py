from __future__ import annotations

from typing import Any, TypedDict


class AgentState(TypedDict, total=False):
    user_input: str
    ticket_id: str
    ticket_context: dict[str, Any]
    access_check: dict[str, Any]
    evidence: list[dict[str, str]]
    final_answer: str
    analysis: dict[str, Any]


def create_initial_state(user_input: str) -> AgentState:
    ticket_id = "TCK-4821" if "4821" in user_input else user_input.strip().split()[-1]
    return {"user_input": user_input, "ticket_id": ticket_id, "evidence": []}

