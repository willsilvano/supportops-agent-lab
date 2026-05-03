from __future__ import annotations

import argparse
from datetime import datetime, timezone
from typing import Any

from supportops_agent.data_loader import (
    filter_by,
    find_by_id,
    list_docs,
    load_collection,
    load_doc,
    save_collection,
    user_has_access,
    user_roles,
)
from supportops_agent.mock_api.schemas import TicketAnalysisInput, TicketNoteInput


def ok(data: Any) -> dict[str, Any]:
    return {"ok": True, "data": data}


def error(message: str) -> dict[str, Any]:
    return {"ok": False, "error": message}


def resolve_mock_route(path: str, method: str = "GET", body: dict[str, Any] | None = None) -> tuple[int, dict[str, Any]]:
    clean_path, _, query = path.partition("?")
    parts = [part for part in clean_path.strip("/").split("/") if part]
    query_params = dict(param.split("=", 1) for param in query.split("&") if "=" in param)

    if method == "GET" and clean_path == "/health":
        return 200, ok({"service": "supportops-mock-api", "status": "ok"})

    collection_routes = {
        "/tickets": "tickets",
        "/users": "users",
        "/roles": "roles",
        "/services": "services",
        "/incidents": "incidents",
    }
    if method == "GET" and clean_path in collection_routes:
        return 200, ok(load_collection(collection_routes[clean_path]))

    if method == "GET" and clean_path == "/docs":
        return 200, ok(list_docs())

    if method == "GET" and len(parts) == 2 and parts[0] == "docs":
        item = load_doc(parts[1])
        return (200, ok(item)) if item else (404, error(f"not found: {path}"))

    if method == "GET" and len(parts) == 2 and parts[0] in {"tickets", "users", "roles"}:
        item = find_by_id(parts[0], parts[1])
        return (200, ok(item)) if item else (404, error(f"not found: {path}"))

    if method == "GET" and len(parts) == 3 and parts[0] == "tickets" and parts[2] == "notes":
        return 200, ok(filter_by("ticket_notes", "ticket_id", parts[1]))

    if method == "POST" and len(parts) == 3 and parts[0] == "tickets" and parts[2] == "notes":
        note_input = TicketNoteInput.model_validate(body or {})
        notes = load_collection("ticket_notes")
        note = {
            "id": f"NOTE-{len(notes) + 1}",
            "ticket_id": parts[1],
            "author": note_input.author,
            "body": note_input.body,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        notes.append(note)
        save_collection("ticket_notes", notes)
        return 201, ok(note)

    if method == "GET" and len(parts) == 3 and parts[0] == "users" and parts[2] == "roles":
        return 200, ok(user_roles(parts[1]))

    if method == "GET" and len(parts) == 3 and parts[0] == "roles" and parts[2] == "permissions":
        from supportops_agent.data_loader import role_permissions

        return 200, ok(role_permissions(parts[1]))

    if method == "GET" and clean_path == "/access/check":
        user_id = query_params.get("user_id")
        resource = query_params.get("resource")
        if not user_id or not resource:
            return 400, error("user_id and resource are required")
        return 200, ok(user_has_access(user_id, resource))

    if method == "GET" and len(parts) == 3 and parts[0] == "services" and parts[2] == "status":
        item = find_by_id("services", parts[1])
        return (200, ok(item)) if item else (404, error(f"not found: {path}"))

    if method == "GET" and clean_path == "/incidents/recent":
        service_id = query_params.get("service_id")
        if not service_id:
            return 400, error("service_id is required")
        return 200, ok(filter_by("incidents", "service_id", service_id))

    if method == "GET" and len(parts) == 2 and parts[0] == "incidents":
        item = find_by_id("incidents", parts[1])
        return (200, ok(item)) if item else (404, error(f"not found: {path}"))

    if method == "GET" and clean_path == "/audit-logs":
        user_id = query_params.get("user_id")
        return 200, ok(filter_by("audit_logs", "user_id", user_id)) if user_id else (400, error("user_id is required"))

    if method == "GET" and clean_path == "/deployments/recent":
        service_id = query_params.get("service_id")
        return 200, ok(filter_by("deployments", "service_id", service_id)) if service_id else (400, error("service_id is required"))

    if method == "GET" and clean_path == "/feature-flags":
        service_id = query_params.get("service_id")
        return 200, ok(filter_by("feature_flags", "service_id", service_id)) if service_id else (400, error("service_id is required"))

    if method == "GET" and len(parts) == 2 and parts[0] == "sla-policies":
        item = find_by_id("sla_policies", parts[1])
        return (200, ok(item)) if item else (404, error(f"not found: {path}"))

    if method == "POST" and clean_path == "/ticket-analysis":
        analysis = TicketAnalysisInput.model_validate(body or {})
        return 201, ok(analysis.model_dump())

    return 404, error(f"not found: {method} {path}")


def _json_response(path: str, method: str = "GET", body: dict[str, Any] | None = None):
    from fastapi.responses import JSONResponse

    status, payload = resolve_mock_route(path, method=method, body=body)
    if status >= 400:
        return JSONResponse(status_code=status, content=payload)
    if status == 201:
        return JSONResponse(status_code=status, content=payload)
    return payload


def create_app():
    try:
        from fastapi import FastAPI
    except ImportError as exc:
        raise RuntimeError("FastAPI nao esta instalado. Rode `python run.py setup`.") from exc

    app = FastAPI(
        title="SupportOps Mock API",
        version="0.1.0",
        description="Mock API local para tickets, usuarios, roles, servicos, incidentes e analises.",
    )

    @app.get("/health")
    def health():
        return _json_response("/health")

    @app.get("/tickets")
    def list_tickets():
        return _json_response("/tickets")

    @app.get("/tickets/{ticket_id}")
    def get_ticket(ticket_id: str):
        return _json_response(f"/tickets/{ticket_id}")

    @app.get("/tickets/{ticket_id}/notes")
    def get_ticket_notes(ticket_id: str):
        return _json_response(f"/tickets/{ticket_id}/notes")

    @app.post("/tickets/{ticket_id}/notes")
    def create_ticket_note(ticket_id: str, payload: TicketNoteInput):
        return _json_response(f"/tickets/{ticket_id}/notes", method="POST", body=payload.model_dump())

    @app.get("/users")
    def list_users():
        return _json_response("/users")

    @app.get("/users/{user_id}")
    def get_user(user_id: str):
        return _json_response(f"/users/{user_id}")

    @app.get("/users/{user_id}/roles")
    def get_user_roles(user_id: str):
        return _json_response(f"/users/{user_id}/roles")

    @app.get("/roles/{role_id}")
    def get_role(role_id: str):
        return _json_response(f"/roles/{role_id}")

    @app.get("/roles/{role_id}/permissions")
    def get_role_permissions(role_id: str):
        return _json_response(f"/roles/{role_id}/permissions")

    @app.get("/access/check")
    def check_access(user_id: str, resource: str):
        return _json_response(f"/access/check?user_id={user_id}&resource={resource}")

    @app.get("/services")
    def list_services():
        return _json_response("/services")

    @app.get("/services/{service_id}/status")
    def get_service_status(service_id: str):
        return _json_response(f"/services/{service_id}/status")

    @app.get("/incidents")
    def list_incidents():
        return _json_response("/incidents")

    @app.get("/incidents/recent")
    def get_recent_incidents(service_id: str):
        return _json_response(f"/incidents/recent?service_id={service_id}")

    @app.get("/audit-logs")
    def get_audit_logs(user_id: str):
        return _json_response(f"/audit-logs?user_id={user_id}")

    @app.get("/deployments/recent")
    def get_recent_deployments(service_id: str):
        return _json_response(f"/deployments/recent?service_id={service_id}")

    @app.get("/feature-flags")
    def get_feature_flags(service_id: str):
        return _json_response(f"/feature-flags?service_id={service_id}")

    @app.get("/sla-policies/{tier}")
    def get_sla_policy(tier: str):
        return _json_response(f"/sla-policies/{tier}")

    @app.get("/docs")
    def docs():
        return _json_response("/docs")

    @app.get("/docs/{slug}")
    def get_doc(slug: str):
        return _json_response(f"/docs/{slug}")

    @app.post("/ticket-analysis")
    def create_ticket_analysis(payload: TicketAnalysisInput):
        return _json_response("/ticket-analysis", method="POST", body=payload.model_dump())

    return app


def run_server(host: str = "127.0.0.1", port: int = 8000) -> None:
    try:
        import uvicorn
    except ImportError as exc:
        raise RuntimeError("Uvicorn nao esta instalado. Rode `python run.py setup`.") from exc

    print(f"SupportOps mock API running at http://{host}:{port}")
    print(f"Interactive docs at http://{host}:{port}/docs")
    uvicorn.run(create_app(), host=host, port=port)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    run_server(args.host, args.port)


try:
    app = create_app()
except RuntimeError:
    app = None


if __name__ == "__main__":
    main()
