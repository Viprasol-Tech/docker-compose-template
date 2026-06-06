"""Tests for the CLI.

Part of Docker Compose Template by Viprasol Tech Private Limited (https://viprasol.com).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from dct.cli import main


def test_list_command_succeeds(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["list"]) == 0
    out = capsys.readouterr().out
    assert "postgres" in out
    assert "full-saas" in out


def test_generate_to_stdout(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["generate", "postgres", "--name", "demo"]) == 0
    out = capsys.readouterr().out
    assert "name: demo" in out
    assert "postgres:16-alpine" in out


def test_generate_to_file(tmp_path: Path) -> None:
    target = tmp_path / "docker-compose.yml"
    rc = main(["generate", "mongo", "-o", str(target)])
    assert rc == 0
    assert target.exists()
    assert "mongo" in target.read_text(encoding="utf-8")


def test_generate_unknown_stack_returns_2() -> None:
    assert main(["generate", "nope"]) == 2


def test_generate_bad_port_returns_2() -> None:
    assert main(["generate", "postgres", "--port", "badformat"]) == 2


def test_validate_generated_file(tmp_path: Path) -> None:
    target = tmp_path / "c.yml"
    main(["generate", "postgres-redis", "-o", str(target)])
    assert main(["validate", str(target)]) == 0


def test_validate_bad_file_returns_1(tmp_path: Path) -> None:
    bad = tmp_path / "bad.yml"
    bad.write_text("name: x\n", encoding="utf-8")
    assert main(["validate", str(bad)]) == 1
