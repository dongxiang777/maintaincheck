from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class CheckResult:
    key: str
    label: str
    passed: bool
    weight: int
    detail: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class AuditReport:
    root: str
    score: int
    checks: list[CheckResult]

    def to_dict(self) -> dict[str, object]:
        return {
            "root": self.root,
            "score": self.score,
            "checks": [check.to_dict() for check in self.checks],
        }


def _first_existing(root: Path, *names: str) -> Path | None:
    for name in names:
        path = root / name
        if path.exists():
            return path
    return None


def _has_nonempty_file(root: Path, *names: str) -> bool:
    path = _first_existing(root, *names)
    return bool(path and path.is_file() and path.stat().st_size > 0)


def _has_tests(root: Path) -> bool:
    tests_dir = root / "tests"
    if tests_dir.is_dir():
        return True
    return any(root.glob("test_*.py")) or any(root.glob("**/test_*.py"))


def _has_ci(root: Path) -> bool:
    workflows = root / ".github" / "workflows"
    if not workflows.is_dir():
        return False
    return any(workflows.glob("*.yml")) or any(workflows.glob("*.yaml"))


def _has_issue_templates(root: Path) -> bool:
    template_dir = root / ".github" / "ISSUE_TEMPLATE"
    template_file = root / ".github" / "ISSUE_TEMPLATE.md"
    return template_dir.is_dir() or template_file.is_file()


def run_audit(root: Path) -> AuditReport:
    root = root.resolve()
    checks = [
        CheckResult(
            key="readme",
            label="README.md",
            passed=_has_nonempty_file(root, "README.md", "readme.md"),
            weight=15,
            detail="Project overview and usage instructions",
        ),
        CheckResult(
            key="license",
            label="LICENSE",
            passed=_has_nonempty_file(root, "LICENSE", "LICENSE.md", "LICENSE.txt"),
            weight=15,
            detail="Clear reuse and distribution terms",
        ),
        CheckResult(
            key="tests",
            label="Tests",
            passed=_has_tests(root),
            weight=15,
            detail="Basic confidence that changes can be verified",
        ),
        CheckResult(
            key="ci",
            label="CI workflows",
            passed=_has_ci(root),
            weight=10,
            detail="Automated checks for pull requests and pushes",
        ),
        CheckResult(
            key="contributing",
            label="CONTRIBUTING.md",
            passed=_has_nonempty_file(root, "CONTRIBUTING.md"),
            weight=10,
            detail="Collaboration guidance for contributors",
        ),
        CheckResult(
            key="code_of_conduct",
            label="CODE_OF_CONDUCT.md",
            passed=_has_nonempty_file(root, "CODE_OF_CONDUCT.md"),
            weight=10,
            detail="Community behavior expectations",
        ),
        CheckResult(
            key="security",
            label="SECURITY.md",
            passed=_has_nonempty_file(root, "SECURITY.md"),
            weight=10,
            detail="Private security reporting guidance",
        ),
        CheckResult(
            key="changelog",
            label="CHANGELOG.md",
            passed=_has_nonempty_file(root, "CHANGELOG.md"),
            weight=10,
            detail="Release history for users and maintainers",
        ),
        CheckResult(
            key="issue_templates",
            label="Issue templates",
            passed=_has_issue_templates(root),
            weight=5,
            detail="Structured bug and support reports",
        ),
    ]
    score = sum(check.weight for check in checks if check.passed)
    return AuditReport(root=str(root), score=score, checks=checks)

