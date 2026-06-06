# Contributing

Thanks for your interest in improving Docker Compose Template! 🎉

## Development setup

```bash
python -m pip install -e ".[dev]"
```

## Before you open a PR

Run the full local gate — it must be green:

```bash
python -m ruff check .
python -m ruff format --check .
python -m mypy src
python -m pytest
```

## Guidelines

- Keep the code typed and `mypy --strict` clean.
- Add or update tests for any behavior change; tests must run fully offline.
- New stacks go in `src/dct/stacks.py`; keep service definitions declarative.
- Use clear, conventional commit messages.
- Be respectful — see our [Code of Conduct](CODE_OF_CONDUCT.md).

## Reporting issues

Use the GitHub issue templates for bug reports and feature requests. For security
issues, follow [SECURITY.md](SECURITY.md) instead of opening a public issue.
