from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from supportops_agent.clients.mock_service_client import MockServiceClient


class TicketContextInput(BaseModel):
    """Schema de entrada para busca de contexto do ticket."""

    ticket_id: str = Field(min_length=1, description="ID do ticket (ex: TCK-4821)")


class TicketContextResult(BaseModel):
    """Contexto enriquecido do ticket retornado ao agente."""

    ticket_id: str
    title: str
    customer: str
    status: str
    priority: str
    resource: str
    service_id: str
    user_id: str
    user_name: str
    user_email: str
    user_roles: list[str] = Field(default_factory=list)
    recent_incidents: list[dict[str, Any]] = Field(default_factory=list)
    audit_logs: list[dict[str, Any]] = Field(default_factory=list)
    service_status: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None


def get_ticket_context(
    payload: dict[str, Any],
    client: MockServiceClient | None = None,
) -> dict[str, Any]:
    """Busca ticket, usuário, status do serviço, incidentes e audit logs.

    Retorna contexto enriquecido e normalizado para o agente.
    """
    # 1. Validar entrada
    validated = TicketContextInput.model_validate(payload)

    if client is None:
        client = MockServiceClient()

    # 2. Buscar ticket
    ticket_resp = client.get_json(f"/tickets/{validated.ticket_id}")
    if not ticket_resp.get("ok"):
        return TicketContextResult(
            ticket_id=validated.ticket_id,
            title="",
            customer="",
            status="unknown",
            priority="unknown",
            resource="",
            service_id="",
            user_id="",
            user_name="",
            user_email="",
            error=ticket_resp.get("error", "Ticket não encontrado"),
        ).model_dump()

    ticket = ticket_resp["data"]
    user_id = ticket.get("user_id", "")
    service_id = ticket.get("service_id", "")

    # 3. Buscar usuário
    user_resp = client.get_json(f"/users/{user_id}")
    user = user_resp.get("data", {}) if user_resp.get("ok") else {}

    # 4. Buscar roles do usuário
    roles_resp = client.get_json(f"/users/{user_id}/roles")
    roles_data = roles_resp.get("data", []) if roles_resp.get("ok") else []
    role_names = [r.get("name", r.get("id", "")) for r in roles_data]

    # 5. Buscar status do serviço
    service_resp = client.get_json(f"/services/{service_id}/status")
    service_data = service_resp.get("data", {}) if service_resp.get("ok") else {}

    # 6. Buscar incidentes recentes
    incidents_resp = client.get_json(f"/incidents/recent?service_id={service_id}")
    incidents_data = incidents_resp.get("data", []) if incidents_resp.get("ok") else []

    # 7. Buscar audit logs
    audit_resp = client.get_json(f"/audit-logs?user_id={user_id}")
    audit_data = audit_resp.get("data", []) if audit_resp.get("ok") else []

    # 8. Montar resultado normalizado
    result = TicketContextResult(
        ticket_id=validated.ticket_id,
        title=ticket.get("title", ""),
        customer=ticket.get("customer", ""),
        status=ticket.get("status", ""),
        priority=ticket.get("priority", ""),
        resource=ticket.get("resource", ""),
        service_id=service_id,
        user_id=user_id,
        user_name=user.get("name", ""),
        user_email=user.get("email", ""),
        user_roles=role_names,
        recent_incidents=incidents_data,
        audit_logs=audit_data,
        service_status=service_data,
        error=None,
    )

    return result.model_dump()
