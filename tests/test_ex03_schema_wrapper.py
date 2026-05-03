import unittest

from supportops_agent.mock_api.server import resolve_mock_route
from supportops_agent.tools.access_tools import CheckUserAccessInput, check_user_access


class LocalClient:
    def check_access(self, user_id, resource):
        status, payload = resolve_mock_route(f"/access/check?user_id={user_id}&resource={resource}")
        self.status = status
        return payload


class Ex03SchemaWrapperTest(unittest.TestCase):
    def test_check_user_access_schema_rejects_empty_user(self):
        with self.assertRaises(Exception):
            CheckUserAccessInput.model_validate({"user_id": "", "resource": "dashboard:revenue"})

    def test_check_user_access_normalizes_api_response(self):
        result = check_user_access(
            {"user_id": "USR-1001", "resource": "dashboard:revenue"},
            client=LocalClient(),
        )
        self.assertEqual(result["user_id"], "USR-1001")
        self.assertTrue(result["allowed"])
        self.assertIn("sales_manager", result["roles"])
        self.assertIn("matched_permissions", result)


if __name__ == "__main__":
    unittest.main()

