"""Tests for compose generation.

Part of Docker Compose Template by Viprasol Tech Private Limited (https://viprasol.com).
"""

from __future__ import annotations

import yaml

from dct.generator import build_compose, render_compose
from dct.models import GenerateOptions
from dct.stacks import get_stack


def test_postgres_generation_produces_expected_service() -> None:
    doc = build_compose(get_stack("postgres"))
    assert "postgres" in doc["services"]
    svc = doc["services"]["postgres"]
    assert svc["image"] == "postgres:16-alpine"
    assert svc["ports"] == ["5432:5432"]


def test_project_name_propagates_to_container_and_top_level() -> None:
    opts = GenerateOptions(project_name="shop")
    doc = build_compose(get_stack("postgres"), opts)
    assert doc["name"] == "shop"
    assert doc["services"]["postgres"]["container_name"] == "shop_postgres"


def test_port_override_changes_host_port_only() -> None:
    opts = GenerateOptions(port_overrides={"postgres": 6543})
    doc = build_compose(get_stack("postgres"), opts)
    assert doc["services"]["postgres"]["ports"] == ["6543:5432"]


def test_no_volumes_option_omits_volumes() -> None:
    opts = GenerateOptions(with_volumes=False)
    doc = build_compose(get_stack("postgres"), opts)
    assert "volumes" not in doc
    assert "volumes" not in doc["services"]["postgres"]


def test_rendered_yaml_round_trips() -> None:
    text = render_compose(get_stack("postgres-redis"))
    parsed = yaml.safe_load(text)
    assert set(parsed["services"]) == {"postgres", "redis"}


def test_depends_on_pruned_to_stack_services() -> None:
    # fastapi-postgres includes the api service which depends on postgres.
    doc = build_compose(get_stack("fastapi-postgres"))
    assert doc["services"]["api"]["depends_on"] == ["postgres"]


def test_full_saas_renders_all_services() -> None:
    text = render_compose(get_stack("full-saas"))
    parsed = yaml.safe_load(text)
    assert set(parsed["services"]) == {"api", "postgres", "redis", "elasticsearch"}


def test_restart_policy_applied() -> None:
    opts = GenerateOptions(restart_policy="always")
    doc = build_compose(get_stack("mongo"), opts)
    assert doc["services"]["mongo"]["restart"] == "always"
