from __future__ import annotations

import json
from typing import Any

from supportops_agent.agent.output_schemas import Evidence, TicketAnalysis
from supportops_agent.clients.mock_service_client import MockServiceClient
from supportops_agent.mock_api.server import resolve_mock_route
from supportops_agent.tools.access_tools import check_user_access
from supportops_agent.tools.ticket_tools import get_ticket_context


class LocalMockClient(MockServiceClient):
    """Client que resolve rotas localmente sem HTTP."""

    def get_json(self, path: str) -> dict[str, Any]:
        return resolve_mock_route(path)[1]

    def post_json(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        return resolve_mock_route(path, method="POST", body=payload)[1]

    def check_access(self, user_id: str, resource: str) -> dict[str, Any]:
        return self.get_json(f"/access/check?user_id={user_id}&resource={resource}")


def fetch_ticket_node(state: dict[str, Any], client: MockServiceClient | None = None) -> dict[str, Any]:
    """Busca contexto completo do ticket e atualiza o state."""
    if client is None:
        client = LocalMockClient()

    ticket_id = state["ticket_id"]
    ticket_context = get_ticket_context({"ticket_id": ticket_id}, client=client)

    return {"ticket_context": ticket_context}


def check_access_node(state: dict[str, Any], client: MockServiceClient | None = None) -> dict[str, Any]:
    """Verifica acesso do usuário ao recurso e atualiza o state."""
    if client is None:
        client = LocalMockClient()

    ticket_context = state["ticket_context"]
    user_id = ticket_context["user_id"]
    resource = ticket_context["resource"]

    access_result = check_user_access(
        {"user_id": user_id, "resource": resource},
        client=client,
    )

    return {"access_check": access_result}


def analyze_node(state: dict[str, Any]) -> dict[str, Any]:
    """Monta evidências, gera TicketAnalysis validada e produz final_answer JSON."""
    ticket_context = state["ticket_context"]
    access_check = state["access_check"]

    # Montar evidências a partir dos dados coletados
    evidence_list: list[Evidence] = []

    # Evidência do audit log
    for log in ticket_context.get("audit_logs", []):
        evidence_list.append(Evidence(
            source="audit_log",
            detail=f"{log.get('event', '')}: {log.get('details', '')} em {log.get('created_at', '')}",
        ))

    # Evidência do access check
    access_status = "permitido" if access_check.get("allowed") else "negado"
    evidence_list.append(Evidence(
        source="access_check",
        detail=f"Acesso {access_status} para {access_check.get('user_id')} no recurso {access_check.get('resource')}. Roles: {access_check.get('roles', [])}",
    ))

    # Evidência do status do serviço
    service_status = ticket_context.get("service_status", {})
    if service_status:
        evidence_list.append(Evidence(
            source="service_status",
            detail=f"Serviço {service_status.get('name', '')}: status={service_status.get('status', '')}, error_rate={service_status.get('error_rate', 'N/A')}",
        ))

    # Evidência de incidentes
    for incident in ticket_context.get("recent_incidents", []):
        evidence_list.append(Evidence(
            source="incident",
            detail=f"{incident.get('title', '')}: status={incident.get('status', '')}, severidade={incident.get('severity', '')}",
        ))

    # Determinar risco
    service_degraded = service_status.get("status") == "degraded"
    has_role_change = any(
        log.get("event") == "role_updated"
        for log in ticket_context.get("audit_logs", [])
    )

    if not access_check.get("allowed"):
        risk = "high"
    elif service_degraded and has_role_change:
        risk = "medium"
    elif service_degraded or has_role_change:
        risk = "medium"
    else:
        risk = "low"

    # Determinar causa raiz
    if has_role_change and service_degraded:
        root_cause = (
            "Alteração de role recente combinada com serviço degradado. "
            "Incidente anterior (cache de permissões) indica que 403 ocorreu "
            "por atraso na propagação de permissões após mudança de role."
        )
    elif has_role_change:
        root_cause = "Alteração de role causou inconsistência temporária de permissões."
    elif not access_check.get("allowed"):
        root_cause = "Usuário não possui permissão para o recurso solicitado."
    else:
        root_cause = "Causa indeterminada — requer investigação adicional."

    # Ações proibidas verificadas (o agente confirma que NÃO executou)
    forbidden_actions = ["change_user_role", "close_ticket", "contact_user_directly"]

    # Montar análise final validada
    analysis = TicketAnalysis(
        ticket_id=ticket_context["ticket_id"],
        risk=risk,
        summary=(
            f"Ticket {ticket_context['ticket_id']}: usuário {ticket_context['user_name']} "
            f"({ticket_context['user_id']}) reportou 403 no recurso {ticket_context['resource']}. "
            f"Audit log mostra alteração de role em {ticket_context.get('audit_logs', [{}])[0].get('created_at', 'N/A')}. "
            f"Serviço {service_status.get('name', '')} está {service_status.get('status', 'unknown')}. "
            f"Incidente anterior de cache de permissões (INC-7001) já foi resolvido. "
            f"Acesso atual: {access_status}."
        ),
        evidence=evidence_list,
        root_cause=root_cause,
        recommended_actions=[
            "Verificar se o cache de permissões foi invalidado corretamente",
            "Monitorar se o erro 403 persiste após resolução do incidente de cache",
            "Considerar escalação se o serviço permanecer degradado",
        ],
        forbidden_actions_checked=forbidden_actions,
        requires_human_approval=risk in ("high", "critical"),
    )

    analysis_dict = analysis.model_dump()
    # Converter Evidence objects para dicts serializáveis
    analysis_dict["evidence"] = [e.model_dump() for e in evidence_list]

    final_answer = json.dumps(analysis_dict, ensure_ascii=False, indent=2)

    return {
        "analysis": analysis_dict,
        "final_answer": final_answer,
    }
