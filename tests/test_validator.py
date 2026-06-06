"""Tests for compose validation.

Part of Docker Compose Template by Viprasol Tech Private Limited (https://viprasol.com).
"""

from __future__ import annotations

from dct.generator import render_compose
from dct.stacks import get_stack
from dct.validator import validate_text


def test_generated_output_validates() -> None:
    text = render_compose(get_stack("full-saas"))
    result = validate_text(text)
    assert result.ok, result.errors
    assert len(result.service_names) == 4


def test_missing_services_is_invalid() -> None:
    result = validate_text("name: x\n")
    assert not result.ok
    assert any("services" in e for e in result.errors)


def test_invalid_yaml_is_caught() -> None:
    result = validate_text("services: [unclosed\n")
    assert not result.ok
    assert any("invalid YAML" in e for e in result.errors)


def test_service_without_image_is_invalid() -> None:
    result = validate_text("services:\n  web:\n    ports: []\n")
    assert not result.ok
    assert any("image" in e for e in result.errors)


def test_unknown_dependency_is_invalid() -> None:
    text = "services:\n  web:\n    image: nginx\n    depends_on:\n      - ghost\n"
    result = validate_text(text)
    assert not result.ok
    assert any("ghost" in e for e in result.errors)


def test_ports_must_be_list() -> None:
    result = validate_text("services:\n  web:\n    image: nginx\n    ports: 80\n")
    assert not result.ok
    assert any("ports" in e for e in result.errors)
