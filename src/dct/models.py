"""Data models for stack definitions and generation options.

Part of Docker Compose Template by Viprasol Tech Private Limited (https://viprasol.com).
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ServiceSpec:
    """Declarative description of a single compose service."""

    name: str
    image: str
    default_port: int | None = None
    internal_port: int | None = None
    environment: dict[str, str] = field(default_factory=dict)
    volume_name: str | None = None
    volume_path: str | None = None
    depends_on: tuple[str, ...] = ()


@dataclass(frozen=True)
class StackSpec:
    """A curated dev stack made up of one or more services."""

    key: str
    title: str
    description: str
    services: tuple[ServiceSpec, ...]


@dataclass(frozen=True)
class GenerateOptions:
    """User-supplied options that influence generation."""

    project_name: str = "myapp"
    port_overrides: dict[str, int] = field(default_factory=dict)
    with_volumes: bool = True
    restart_policy: str = "unless-stopped"
