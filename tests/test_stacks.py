"""Tests for the stack catalog.

Part of Docker Compose Template by Viprasol Tech Private Limited (https://viprasol.com).
"""

from __future__ import annotations

import pytest

from dct.stacks import get_stack, list_stacks, stack_keys


def test_catalog_has_expected_stacks() -> None:
    keys = set(stack_keys())
    assert {"postgres", "postgres-redis", "fastapi-postgres", "mongo", "full-saas"} <= keys


def test_list_stacks_sorted_and_nonempty() -> None:
    stacks = list_stacks()
    assert stacks
    assert [s.key for s in stacks] == sorted(s.key for s in stacks)


def test_every_stack_has_services() -> None:
    for stack in list_stacks():
        assert stack.services, f"{stack.key} has no services"


def test_get_unknown_stack_raises() -> None:
    with pytest.raises(KeyError):
        get_stack("does-not-exist")


def test_full_saas_contains_four_services() -> None:
    stack = get_stack("full-saas")
    names = {svc.name for svc in stack.services}
    assert names == {"api", "postgres", "redis", "elasticsearch"}
