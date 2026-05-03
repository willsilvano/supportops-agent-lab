import unittest

from supportops_agent.mock_api.server import resolve_mock_route


class Ex01MockApiTest(unittest.TestCase):
    def test_ticket_user_service_and_incidents_routes(self):
        status, ticket_payload = resolve_mock_route("/tickets/TCK-4821")
        self.assertEqual(status, 200)
        ticket = ticket_payload["data"]

        status, user_payload = resolve_mock_route(f"/users/{ticket['user_id']}")
        self.assertEqual(status, 200)
        self.assertEqual(user_payload["data"]["name"], "Maria Silva")

        status, access_payload = resolve_mock_route(
            f"/access/check?user_id={ticket['user_id']}&resource={ticket['resource']}"
        )
        self.assertEqual(status, 200)
        self.assertTrue(access_payload["data"]["allowed"])

        status, service_payload = resolve_mock_route(f"/services/{ticket['service_id']}/status")
        self.assertEqual(status, 200)
        self.assertEqual(service_payload["data"]["status"], "degraded")

        status, incidents_payload = resolve_mock_route(f"/incidents/recent?service_id={ticket['service_id']}")
        self.assertEqual(status, 200)
        self.assertGreaterEqual(len(incidents_payload["data"]), 1)

    def test_api_exposes_at_least_15_supportops_capabilities(self):
        routes = [
            "/health",
            "/tickets",
            "/tickets/TCK-4821",
            "/tickets/TCK-4821/notes",
            "/users",
            "/users/USR-1001",
            "/users/USR-1001/roles",
            "/roles/ROLE-SALES-MANAGER",
            "/roles/ROLE-SALES-MANAGER/permissions",
            "/access/check?user_id=USR-1001&resource=dashboard:revenue",
            "/services",
            "/services/analytics-api/status",
            "/incidents",
            "/incidents/recent?service_id=analytics-api",
            "/audit-logs?user_id=USR-1001",
            "/deployments/recent?service_id=analytics-api",
            "/feature-flags?service_id=analytics-api",
            "/sla-policies/enterprise",
            "/docs",
            "/docs/runbook-auth",
        ]
        ok_routes = [route for route in routes if resolve_mock_route(route)[0] == 200]
        self.assertGreaterEqual(len(ok_routes), 15)


if __name__ == "__main__":
    unittest.main()

