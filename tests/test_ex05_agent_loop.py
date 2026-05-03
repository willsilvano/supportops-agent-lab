import json
import unittest

from supportops_agent.agent.graph import run_supportops_flow


class Ex05AgentLoopTest(unittest.TestCase):
    def test_supportops_flow_returns_valid_analysis(self):
        result = run_supportops_flow("Analise o ticket TCK-4821")
        self.assertIn("ticket_context", result)
        self.assertIn("access_check", result)
        analysis = result["analysis"]
        self.assertEqual(analysis["ticket_id"], "TCK-4821")
        self.assertEqual(analysis["risk"], "medium")
        self.assertIn("change_user_role", analysis["forbidden_actions_checked"])

    def test_final_answer_is_json(self):
        result = run_supportops_flow("Analise o ticket TCK-4821")
        parsed = json.loads(result["final_answer"])
        self.assertEqual(parsed["ticket_id"], "TCK-4821")


if __name__ == "__main__":
    unittest.main()

