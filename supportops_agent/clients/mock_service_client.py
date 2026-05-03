from __future__ import annotations

import json
import os
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


DEFAULT_BASE_URL = os.getenv("SUPPORTOPS_BASE_URL", "http://127.0.0.1:8000")


class MockServiceClient:
    def __init__(self, base_url: str = DEFAULT_BASE_URL, timeout: float = 2.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def get_json(self, path: str) -> dict[str, Any]:
        return self._request_json("GET", path)

    def post_json(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self._request_json("POST", path, payload)

    def _request_json(self, method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        data = None if payload is None else json.dumps(payload).encode("utf-8")
        request = Request(
            f"{self.base_url}{path}",
            data=data,
            method=method,
            headers={"Content-Type": "application/json"},
        )
        try:
            with urlopen(request, timeout=self.timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            body = exc.read().decode("utf-8")
            try:
                return json.loads(body)
            except json.JSONDecodeError:
                return {"ok": False, "error": f"http {exc.code}"}
        except URLError as exc:
            return {"ok": False, "error": f"mock service unavailable: {exc.reason}"}

    def get_ticket(self, ticket_id: str) -> dict[str, Any]:
        return self.get_json(f"/tickets/{quote(ticket_id)}")

    def get_user(self, user_id: str) -> dict[str, Any]:
        return self.get_json(f"/users/{quote(user_id)}")

    def get_user_roles(self, user_id: str) -> dict[str, Any]:
        return self.get_json(f"/users/{quote(user_id)}/roles")

    def check_access(self, user_id: str, resource: str) -> dict[str, Any]:
        return self.get_json(f"/access/check?user_id={quote(user_id)}&resource={quote(resource)}")

    def get_service_status(self, service_id: str) -> dict[str, Any]:
        return self.get_json(f"/services/{quote(service_id)}/status")

    def get_recent_incidents(self, service_id: str) -> dict[str, Any]:
        return self.get_json(f"/incidents/recent?service_id={quote(service_id)}")

    def get_audit_logs(self, user_id: str) -> dict[str, Any]:
        return self.get_json(f"/audit-logs?user_id={quote(user_id)}")


def check_mock_service_health(client: MockServiceClient | None = None) -> bool:
    client = client or MockServiceClient()
    try:
        response = client.get_json("/health")
    except Exception:
        return False
    return response.get("ok") is True
