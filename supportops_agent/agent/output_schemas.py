from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


RiskLevel = Literal["low", "medium", "high", "critical"]


class Evidence(BaseModel):
    """Uma evidência coletada durante a investigação."""

    source: str = Field(description="Origem da evidência (ex: audit_log, access_check, service_status)")
    detail: str = Field(description="Descrição do dado relevante encontrado")


class TicketAnalysis(BaseModel):
    """Output estruturado final do agente — validado por código."""

    ticket_id: str
    risk: RiskLevel
    summary: str = Field(max_length=2000)
    evidence: list[Evidence] = Field(min_length=1)
    root_cause: str
    recommended_actions: list[str] = Field(default_factory=list)
    forbidden_actions_checked: list[str] = Field(default_factory=list)
    requires_human_approval: bool = True
