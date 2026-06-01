from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from maintaincheck.checks import run_audit


def _write(path: Path, content: str = "x") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


class RunAuditTests(unittest.TestCase):
    def test_scores_minimal_repo(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write(root / "README.md")
            _write(root / "LICENSE")
            _write(root / "tests" / "test_basic.py")
            _write(root / ".github" / "workflows" / "ci.yml")

            report = run_audit(root)

            self.assertEqual(report.score, 55)
            self.assertEqual(sum(check.passed for check in report.checks), 4)

    def test_scores_complete_repo(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in [
                "README.md",
                "LICENSE",
                "CONTRIBUTING.md",
                "CODE_OF_CONDUCT.md",
                "SECURITY.md",
                "CHANGELOG.md",
            ]:
                _write(root / name)
            _write(root / "tests" / "test_basic.py")
            _write(root / ".github" / "workflows" / "ci.yml")
            _write(root / ".github" / "ISSUE_TEMPLATE" / "bug.md")

            report = run_audit(root)

            self.assertEqual(report.score, 100)
            self.assertTrue(all(check.passed for check in report.checks))


if __name__ == "__main__":
    unittest.main()
