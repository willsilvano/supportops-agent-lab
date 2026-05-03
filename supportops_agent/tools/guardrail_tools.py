from __future__ import annotations

from typing import Any


FORBIDDEN_ACTIONS = {"change_user_role", "grant_permission", "close_ticket", "delete_ticket"}
ALLOWED_TOOLS = {
    "get_ticket_context",
    "check_user_access",
    "get_service_status",
    "get_recent_incidents",
    "search_runbook",
    "create_internal_note",
    "create_ticket_analysis",
}
INJECTION_PATTERNS = [
    "ignore as instrucoes",
    "ignore instrucoes",
    "ignore previous",
    "ignore all previous",
    "feche o ticket",
    "close the ticket",
    "altere a role",
    "change the role",
]


def detect_prompt_injection(text: str) -> dict[str, Any]:
    """TODO Ex11: detecte padroes simples de prompt injection."""
    raise NotImplementedError("Implemente detect_prompt_injection no Ex11.")


def validate_tool_name(tool_name: str) -> dict[str, Any]:
    """TODO Ex11: valide allowlist e bloqueie acoes proibidas."""
    raise NotImplementedError("Implemente validate_tool_name no Ex11.")


def validate_final_analysis(analysis: dict[str, Any]) -> dict[str, Any]:
    """TODO Ex11: rejeite recomendacoes finais com acoes proibidas."""
    raise NotImplementedError("Implemente validate_final_analysis no Ex11.")
