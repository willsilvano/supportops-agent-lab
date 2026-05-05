from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from supportops_agent.clients.mock_service_client import MockServiceClient


class CheckUserAccessInput(BaseModel):
    """Schema de entrada para verificação de acesso do usuário."""

    user_id: str = Field(min_length=1, description="ID do usuário (ex: USR-1001)")
    resource: str = Field(min_length=1, description="Recurso a verificar (ex: dashboard:revenue)")


class CheckUserAccessResult(BaseModel):
    """Payload normalizado retornado ao agente — sem dados internos desnecessários."""

    user_id: str
    resource: str
    allowed: bool
    roles: list[str] = Field(default_factory=list)
    matched_permissions: list[str] = Field(default_factory=list)
    error: str | None = None


def check_user_access(
    payload: dict[str, Any],
    client: MockServiceClient | None = None,
) -> dict[str, Any]:
    """Valida entrada, chama client.check_access e normaliza a resposta.

    O LLM recebe apenas os campos definidos em CheckUserAccessResult,
    nunca a resposta crua da API.
    """
    # 1. Validar entrada via Pydantic
    validated = CheckUserAccessInput.model_validate(payload)

    # 2. Usar client padrão se não fornecido
    if client is None:
        client = MockServiceClient()

    # 3. Chamar a API
    try:
        raw_response = client.check_access(validated.user_id, validated.resource)
    except Exception as exc:
        result = CheckUserAccessResult(
            user_id=validated.user_id,
            resource=validated.resource,
            allowed=False,
            roles=[],
            matched_permissions=[],
            error=f"Falha ao consultar API: {exc}",
        )
        return result.model_dump()

    # 4. Tratar erro da API
    if raw_response.get("ok") is False:
        result = CheckUserAccessResult(
            user_id=validated.user_id,
            resource=validated.resource,
            allowed=False,
            roles=[],
            matched_permissions=[],
            error=raw_response.get("error", "Erro desconhecido"),
        )
        return result.model_dump()

    # 5. Normalizar resposta — extrair apenas o necessário
    data = raw_response.get("data", raw_response)

    # Extrair nomes das permissões (não repassar objetos completos)
    raw_permissions = data.get("matched_permissions", [])
    permission_names = [
        p.get("name", p.get("id", str(p))) if isinstance(p, dict) else str(p)
        for p in raw_permissions
    ]

    result = CheckUserAccessResult(
        user_id=data.get("user_id", validated.user_id),
        resource=data.get("resource", validated.resource),
        allowed=bool(data.get("allowed", False)),
        roles=data.get("roles", []),
        matched_permissions=permission_names,
        error=None,
    )

    return result.model_dump()
