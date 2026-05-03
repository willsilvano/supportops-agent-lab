from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from supportops_agent.clients.mock_service_client import MockServiceClient


class CheckUserAccessInput(BaseModel):
    """TODO Ex03: defina user_id e resource como campos obrigatorios."""


class CheckUserAccessResult(BaseModel):
    """TODO Ex03: defina o payload normalizado retornado ao agente."""


def check_user_access(
    payload: dict[str, Any],
    client: MockServiceClient | None = None,
) -> dict[str, Any]:
    """TODO Ex03: valide entrada, chame client.check_access e normalize a resposta."""
    raise NotImplementedError("Implemente check_user_access no Ex03.")
