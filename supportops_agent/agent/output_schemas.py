from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


RiskLevel = Literal["low", "medium", "high", "critical"]


class Evidence(BaseModel):
    """TODO Ex05: defina source e detail."""


class TicketAnalysis(BaseModel):
    """TODO Ex05: defina o output estruturado final do agente."""
