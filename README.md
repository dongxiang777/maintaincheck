# maintaincheck

[![CI](https://github.com/dongxiang777/maintaincheck/actions/workflows/ci.yml/badge.svg)](https://github.com/dongxiang777/maintaincheck/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-3776AB.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

`maintaincheck` is a small command-line tool that scores the baseline hygiene of an open source repository.

It is built for solo maintainers and early-stage open source projects that want a fast answer to a simple question:

> Is this repo ready for other people to use, review, or contribute to?

## What it checks

`maintaincheck` looks for the files and conventions that make repositories easier to understand, safer to use, and easier to contribute to.

| Check | Weight | Why it matters |
| --- | ---: | --- |
| `README.md` | 15 | Explains what the project does and how to use it |
| `LICENSE` | 15 | Clarifies reuse and distribution rights |
| Tests | 15 | Gives basic confidence that behavior can be verified |
| CI workflows | 10 | Keeps validation automatic on push and PR |
| `CONTRIBUTING.md` | 10 | Tells contributors how to participate |
| `CODE_OF_CONDUCT.md` | 10 | Sets collaboration expectations |
| `SECURITY.md` | 10 | Provides a path for responsible disclosure |
| `CHANGELOG.md` | 10 | Tracks releases and project changes |
| Issue templates | 5 | Helps structure bug reports and feedback |

## Why this exists

Many small open source repos are useful long before they are polished. The problem is that missing maintenance files can make a project look abandoned, risky, or hard to contribute to even when the code itself is solid.

`maintaincheck` gives maintainers a quick signal before publishing a repo, opening it to contributors, or wiring it into CI.

## Install

Install from the local checkout:

```bash
pip install .
```

Install directly from GitHub:

```bash
pip install git+https://github.com/dongxiang777/maintaincheck.git
```

## Usage

Audit the current repository:

```bash
maintaincheck
```

Audit another path:

```bash
maintaincheck /path/to/repo
```

Emit machine-readable JSON:

```bash
maintaincheck --json
```

Fail CI if the score is too low:

```bash
maintaincheck --min-score 80
```

## Sample output

```text
maintaincheck report for /work/my-repo
Score: 85/100

[PASS] README.md
[PASS] LICENSE
[PASS] Tests
[PASS] CI workflows
[PASS] CONTRIBUTING.md
[PASS] CODE_OF_CONDUCT.md
[PASS] SECURITY.md
[FAIL] CHANGELOG.md
[PASS] Issue templates
```

## JSON output

```json
{
  "root": "/work/my-repo",
  "score": 85,
  "checks": [
    {
      "key": "readme",
      "label": "README.md",
      "passed": true,
      "weight": 15,
      "detail": "Project overview and usage instructions"
    }
  ]
}
```

## Use cases

- Run it locally before making a repository public
- Gate pull requests with a minimum repository score
- Use it as a lightweight checklist for new OSS projects
- Audit template repos before reusing them across teams

## Development

```bash
uv run pytest
uv run python -m maintaincheck
uv run python -m maintaincheck --min-score 100
```

## Roadmap

- Add configurable checks and custom weights
- Export markdown or badge-friendly summaries
- Package a reusable GitHub Action wrapper

## License

MIT
