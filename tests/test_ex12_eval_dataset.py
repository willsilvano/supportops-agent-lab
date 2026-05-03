import unittest

from supportops_agent.evals.dataset import load_eval_cases


class Ex12EvalDatasetTest(unittest.TestCase):
    def test_eval_cases_have_required_fields(self):
        cases = load_eval_cases()
        self.assertGreaterEqual(len(cases), 2)
        first = cases[0]
        self.assertTrue(first.id)
        self.assertTrue(first.input)
        self.assertTrue(first.expected_tools)
        self.assertTrue(first.reference_answer)

    def test_dataset_contains_adversarial_case(self):
        cases = load_eval_cases()
        joined = " ".join(case.input.lower() for case in cases)
        self.assertIn("ignore", joined)


if __name__ == "__main__":
    unittest.main()

