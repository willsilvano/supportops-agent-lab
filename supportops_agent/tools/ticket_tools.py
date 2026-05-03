from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from supportops_agent.clients.mock_service_client import MockServiceClient


class TicketContextInput(BaseModel):
    """TODO Ex05: defina ticket_id como campo obrigatorio."""


class TicketContextResult(BaseModel):
    """TODO Ex05: defina o contexto enriquecido que o agente vai consumir."""


def get_ticket_context(
    payload: dict[str, Any],
    client: MockServiceClient | None = None,
) -> dict[str, Any]:
    """TODO Ex05: busque ticket, usuario, status, incidentes e audit logs."""
    raise NotImplementedError("Implemente get_ticket_context no Ex05.")
