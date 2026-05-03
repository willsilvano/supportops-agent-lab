from __future__ import annotations

import json
from pathlib import Path
from typing import Any


DATA_DIR = Path(__file__).resolve().parent / "data"
DOCS_DIR = DATA_DIR / "docs"


def load_collection(name: str) -> list[dict[str, Any]]:
    path = DATA_DIR / f"{name}.json"
    return json.loads(path.read_text(encoding="utf-8"))


def save_collection(name: str, items: list[dict[str, Any]]) -> None:
    path = DATA_DIR / f"{name}.json"
    path.write_text(json.dumps(items, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def find_by_id(collection: str, item_id: str) -> dict[str, Any] | None:
    for item in load_collection(collection):
        if item.get("id") == item_id:
            return item
    return None


def filter_by(collection: str, field: str, value: str) -> list[dict[str, Any]]:
    return [item for item in load_collection(collection) if item.get(field) == value]


def list_docs() -> list[dict[str, str]]:
    docs = []
    for path in sorted(DOCS_DIR.glob("*.md")):
        docs.append({"slug": path.stem, "path": str(path.relative_to(DATA_DIR))})
    return docs


def load_doc(slug: str) -> dict[str, str] | None:
    path = DOCS_DIR / f"{slug}.md"
    if not path.exists():
        return None
    return {"slug": slug, "text": path.read_text(encoding="utf-8")}


def role_permissions(role_id: str) -> list[dict[str, Any]]:
    role = find_by_id("roles", role_id)
    if role is None:
        return []
    permissions = load_collection("permissions")
    permission_ids = set(role.get("permission_ids", []))
    return [permission for permission in permissions if permission["id"] in permission_ids]


def user_roles(user_id: str) -> list[dict[str, Any]]:
    user = find_by_id("users", user_id)
    if user is None:
        return []
    roles = load_collection("roles")
    role_ids = set(user.get("role_ids", []))
    return [role for role in roles if role["id"] in role_ids]


def user_has_access(user_id: str, resource: str) -> dict[str, Any]:
    roles = user_roles(user_id)
    matched_permissions: list[dict[str, Any]] = []
    for role in roles:
        for permission in role_permissions(role["id"]):
            permission_resource = permission.get("resource")
            if permission_resource == resource or permission_resource == resource.split(":")[0] + ":*":
                matched_permissions.append(permission)

    return {
        "user_id": user_id,
        "resource": resource,
        "allowed": bool(matched_permissions),
        "roles": [role["name"] for role in roles],
        "matched_permissions": matched_permissions,
    }
