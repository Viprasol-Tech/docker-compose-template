<p align="center"><img src="docs/assets/logo.png" width="120"></p>

# Docker Compose Template

> Scaffold production-shaped local dev stacks in seconds — pick a curated stack, generate a valid `docker-compose.yml`, and validate it, all offline.

*Built and maintained by [Viprasol Tech](https://viprasol.com) — Fintech Experts. Full-Stack Builders.*

![CI](https://img.shields.io/github/actions/workflow/status/Viprasol-Tech/docker-compose-template/ci.yml?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)
![Python](https://img.shields.io/badge/python-3.11%2B-blue?style=flat-square)
![Ruff](https://img.shields.io/badge/lint-ruff-261230?style=flat-square)
![Telegram](https://img.shields.io/badge/Telegram-viprasol__help-26A5E4?style=flat-square)
![Stars](https://img.shields.io/github/stars/Viprasol-Tech/docker-compose-template?style=flat-square)

## ✨ Features

- 🐳 Generate valid `docker-compose.yml` from curated dev stacks
- 📦 Curated catalog: Postgres, Postgres+Redis, FastAPI+Postgres, Mongo, Elasticsearch, full-SaaS
- ⚙️ Options for project name, host ports, volumes, and restart policy
- 🗂️ Ready-to-use compose files shipped in `/stacks`
- ✅ Built-in `validate` command that parses and sanity-checks YAML
- 🔌 Clean Python API (`build_compose`, `render_compose`, `validate_text`)
- 🧪 12+ fully offline tests — no Docker daemon or network needed
- 🪶 Tiny footprint: one dependency (PyYAML)
- 🧰 Typed (`mypy --strict`) and linted (`ruff`)
- 🚀 Single `dct` CLI entry point

## 🚀 Quickstart

```bash
python -m pip install -e .
dct list
dct generate fastapi-postgres --name acme --port postgres=6543 -o docker-compose.yml
dct validate docker-compose.yml
```

## 🛠️ Usage example

```python
from dct.generator import render_compose
from dct.models import GenerateOptions
from dct.stacks import get_stack

text = render_compose(
    get_stack("postgres-redis"),
    GenerateOptions(project_name="acme", port_overrides={"postgres": 6543}),
)
print(text)
```

## 🗺️ Roadmap

- [x] Curated stack catalog
- [x] Generator with options
- [x] Offline validator
- [ ] Healthchecks and network customization
- [ ] Profiles and override files
- [ ] Plugin system for custom stacks

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) and our
[Code of Conduct](CODE_OF_CONDUCT.md) before opening a pull request.

## 📬 Contact — Viprasol Tech Private Limited

- 🌐 Website: [viprasol.com](https://viprasol.com)
- ✉️ Email: [support@viprasol.com](mailto:support@viprasol.com)
- 💬 Telegram: [t.me/viprasol_help](https://t.me/viprasol_help) · 📱 WhatsApp: +91 96336 52112
- 🐙 GitHub: [@Viprasol-Tech](https://github.com/Viprasol-Tech) · 💼 [LinkedIn](https://www.linkedin.com/in/viprasol/) · 𝕏 [@viprasol](https://twitter.com/viprasol)

> *Viprasol Tech — fintech software, algorithmic trading systems, MT4/MT5 bots, AI voice agents, and B2B SaaS. Need a custom build? [Get in touch](mailto:support@viprasol.com).*

## 📄 License

Released under the [MIT License](LICENSE) © 2025 Viprasol Tech Private Limited.
