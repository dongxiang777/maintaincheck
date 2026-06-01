# maintaincheck

`maintaincheck` is a tiny command-line tool that audits the basics of an open source repository.

It checks whether a repo includes the files and workflows that make collaboration easier:

- `README.md`
- `LICENSE`
- tests
- CI workflows
- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `SECURITY.md`
- `CHANGELOG.md`
- issue templates

The goal is simple: give maintainers a quick signal before they publish or share a repository.

## Why this exists

Small and solo-maintained projects often skip repository hygiene because setting up process files feels slower than shipping code. This tool helps maintainers catch the most common gaps in a few seconds.

## Install

```bash
pip install .
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

Emit JSON:

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

## Roadmap

- Add custom rule configuration
- Add badge generation
- Add GitHub Action wrapper

## Development

```bash
uv run pytest
uv run python -m maintaincheck
```

## License

MIT
