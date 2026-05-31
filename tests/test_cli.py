import json
import tempfile
import unittest
from pathlib import Path

from llm_cost_guard.cli import analyze_cost, estimate_tokens, run


class LlmCostGuardTests(unittest.TestCase):
    def test_estimates_tokens(self):
        self.assertEqual(estimate_tokens("abcd"), 1)
        self.assertEqual(estimate_tokens("abcde"), 2)

    def test_flags_over_budget(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "prompt.txt"
            path.write_text("x" * 100, encoding="utf-8")
            result = analyze_cost(str(path), rate=1.0, budget=1.0)
        self.assertEqual(result["status"], "over-budget")

    def test_json_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "prompt.txt"
            path.write_text("hello", encoding="utf-8")
            payload = json.loads(run(str(path), 0.01, output_format="json"))
        self.assertIn("estimated_tokens", payload)


if __name__ == "__main__":
    unittest.main()
