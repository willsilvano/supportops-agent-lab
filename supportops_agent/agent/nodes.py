from __future__ import annotations

from typing import Any

from supportops_agent.clients.mock_service_client import MockServiceClient
from supportops_agent.mock_api.server import resolve_mock_route


class LocalMockClient(MockServiceClient):
    def get_json(self, path: str) -> dict[str, Any]:
        return resolve_mock_route(path)[1]

    def post_json(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        return resolve_mock_route(path, method="POST", body=payload)[1]


def fetch_ticket_node(state: dict[str, Any], client: MockServiceClient | None = None) -> dict[str, Any]:
    """TODO Ex05: chame get_ticket_context e atualize ticket_context no state."""
    raise NotImplementedError("Implemente fetch_ticket_node no Ex05.")


def check_access_node(state: dict[str, Any], client: MockServiceClient | None = None) -> dict[str, Any]:
    """TODO Ex05: chame check_user_access e atualize access_check no state."""
    raise NotImplementedError("Implemente check_access_node no Ex05.")


def analyze_node(state: dict[str, Any]) -> dict[str, Any]:
    """TODO Ex05: monte TicketAnalysis, valide schema e gere final_answer JSON."""
    raise NotImplementedError("Implemente analyze_node no Ex05.")
