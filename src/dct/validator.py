"""Validate docker-compose YAML documents.

Part of Docker Compose Template by Viprasol Tech Private Limited (https://viprasol.com).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import yaml


class ValidationError(Exception):
    """Raised when a compose document fails validation."""


@dataclass
class ValidationResult:
    """Outcome of validating a compose document."""

    ok: bool
    errors: list[str] = field(default_factory=list)
    service_names: list[str] = field(default_factory=list)


def _validate_doc(doc: Any) -> ValidationResult:
    errors: list[str] = []

    if not isinstance(doc, dict):
        return ValidationResult(ok=False, errors=["top-level document must be a mapping"])

    services = doc.get("services")
    if services is None:
        errors.append("missing required 'services' key")
        return ValidationResult(ok=False, errors=errors)

    if not isinstance(services, dict) or not services:
        errors.append("'services' must be a non-empty mapping")
        return ValidationResult(ok=False, errors=errors)

    service_names: list[str] = []
    for name, svc in services.items():
        service_names.append(str(name))
        if not isinstance(svc, dict):
            errors.append(f"service {name!r} must be a mapping")
            continue
        if "image" not in svc and "build" not in svc:
            errors.append(f"service {name!r} must define 'image' or 'build'")
        ports = svc.get("ports")
        if ports is not None and not isinstance(ports, list):
            errors.append(f"service {name!r} 'ports' must be a list")
        depends = svc.get("depends_on")
        if isinstance(depends, list):
            for dep in depends:
                if dep not in services:
                    errors.append(f"service {name!r} depends on unknown service {dep!r}")

    return ValidationResult(ok=not errors, errors=errors, service_names=service_names)


def validate_text(text: str) -> ValidationResult:
    """Parse ``text`` as YAML and validate it as a compose document."""
    try:
        doc = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        return ValidationResult(ok=False, errors=[f"invalid YAML: {exc}"])
    return _validate_doc(doc)


def validate_file(path: str) -> ValidationResult:
    """Read ``path`` and validate its contents as a compose document."""
    try:
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
    except OSError as exc:
        return ValidationResult(ok=False, errors=[f"cannot read file: {exc}"])
    return validate_text(text)
