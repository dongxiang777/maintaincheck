from __future__ import annotations

import argparse
import json
from pathlib import Path

from .checks import AuditReport, run_audit


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="maintaincheck",
        description="Audit the hygiene of an open source repository.",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Repository path to audit. Defaults to the current directory.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON output.",
    )
    parser.add_argument(
        "--min-score",
        type=int,
        default=None,
        help="Exit with status 1 when the score is below this value.",
    )
    return parser


def format_text(report: AuditReport) -> str:
    lines = [
        f"maintaincheck report for {report.root}",
        f"Score: {report.score}/100",
        "",
    ]
    for check in report.checks:
        status = "PASS" if check.passed else "FAIL"
        lines.append(f"[{status}] {check.label}")
    return "\n".join(lines)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    report = run_audit(Path(args.path))

    if args.json:
        print(json.dumps(report.to_dict(), indent=2))
    else:
        print(format_text(report))

    if args.min_score is not None and report.score < args.min_score:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

