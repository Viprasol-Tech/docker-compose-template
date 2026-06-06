"""Demo: generate and validate a compose file fully offline.

Part of Docker Compose Template by Viprasol Tech Private Limited (https://viprasol.com).

Run with: python examples/demo.py
"""

from __future__ import annotations

from dct.generator import render_compose
from dct.models import GenerateOptions
from dct.stacks import get_stack, list_stacks
from dct.validator import validate_text


def main() -> None:
    print("Available stacks:")
    for stack in list_stacks():
        print(f"  - {stack.key}: {stack.title}")

    options = GenerateOptions(project_name="acme", port_overrides={"postgres": 6543})
    text = render_compose(get_stack("fastapi-postgres"), options)

    print("\nGenerated docker-compose.yml:\n")
    print(text)

    result = validate_text(text)
    print(f"Validation OK: {result.ok} (services: {', '.join(result.service_names)})")


if __name__ == "__main__":
    main()
