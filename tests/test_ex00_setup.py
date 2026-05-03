import unittest

from supportops_agent.data_loader import find_by_id, load_doc
from supportops_agent.mock_api.server import resolve_mock_route


class Ex00SetupTest(unittest.TestCase):
    def test_core_data_exists(self):
        ticket = find_by_id("tickets", "TCK-4821")
        self.assertIsNotNone(ticket)
        self.assertEqual(ticket["service_id"], "analytics-api")

    def test_docs_exist(self):
        doc = load_doc("runbook-auth")
        self.assertIsNotNone(doc)
        self.assertIn("Erro 403", doc["text"])

    def test_health_route(self):
        status, payload = resolve_mock_route("/health")
        self.assertEqual(status, 200)
        self.assertTrue(payload["ok"])


if __name__ == "__main__":
    unittest.main()

