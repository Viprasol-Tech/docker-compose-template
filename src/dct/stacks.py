"""Curated catalog of dev stacks.

Part of Docker Compose Template by Viprasol Tech Private Limited (https://viprasol.com).
"""

from __future__ import annotations

from .models import ServiceSpec, StackSpec

_POSTGRES = ServiceSpec(
    name="postgres",
    image="postgres:16-alpine",
    default_port=5432,
    internal_port=5432,
    environment={
        "POSTGRES_USER": "postgres",
        "POSTGRES_PASSWORD": "postgres",
        "POSTGRES_DB": "app",
    },
    volume_name="postgres_data",
    volume_path="/var/lib/postgresql/data",
)

_REDIS = ServiceSpec(
    name="redis",
    image="redis:7-alpine",
    default_port=6379,
    internal_port=6379,
    volume_name="redis_data",
    volume_path="/data",
)

_MONGO = ServiceSpec(
    name="mongo",
    image="mongo:7",
    default_port=27017,
    internal_port=27017,
    environment={
        "MONGO_INITDB_ROOT_USERNAME": "root",
        "MONGO_INITDB_ROOT_PASSWORD": "root",
    },
    volume_name="mongo_data",
    volume_path="/data/db",
)

_ELASTIC = ServiceSpec(
    name="elasticsearch",
    image="elasticsearch:8.13.4",
    default_port=9200,
    internal_port=9200,
    environment={
        "discovery.type": "single-node",
        "xpack.security.enabled": "false",
        "ES_JAVA_OPTS": "-Xms512m -Xmx512m",
    },
    volume_name="elastic_data",
    volume_path="/usr/share/elasticsearch/data",
)

_FASTAPI = ServiceSpec(
    name="api",
    image="tiangolo/uvicorn-gunicorn-fastapi:python3.11",
    default_port=8000,
    internal_port=80,
    environment={"MODULE_NAME": "app.main"},
    depends_on=("postgres",),
)

_CATALOG: dict[str, StackSpec] = {
    "postgres": StackSpec(
        key="postgres",
        title="PostgreSQL",
        description="A single PostgreSQL database service.",
        services=(_POSTGRES,),
    ),
    "postgres-redis": StackSpec(
        key="postgres-redis",
        title="PostgreSQL + Redis",
        description="PostgreSQL database plus a Redis cache.",
        services=(_POSTGRES, _REDIS),
    ),
    "fastapi-postgres": StackSpec(
        key="fastapi-postgres",
        title="FastAPI + PostgreSQL",
        description="A FastAPI app wired to a PostgreSQL database.",
        services=(_FASTAPI, _POSTGRES),
    ),
    "mongo": StackSpec(
        key="mongo",
        title="MongoDB",
        description="A single MongoDB document database service.",
        services=(_MONGO,),
    ),
    "elasticsearch": StackSpec(
        key="elasticsearch",
        title="Elasticsearch",
        description="A single-node Elasticsearch service for local search.",
        services=(_ELASTIC,),
    ),
    "full-saas": StackSpec(
        key="full-saas",
        title="Full SaaS",
        description="FastAPI + PostgreSQL + Redis + Elasticsearch for a complete SaaS stack.",
        services=(_FASTAPI, _POSTGRES, _REDIS, _ELASTIC),
    ),
}


def list_stacks() -> list[StackSpec]:
    """Return all curated stacks, sorted by key."""
    return [_CATALOG[k] for k in sorted(_CATALOG)]


def get_stack(key: str) -> StackSpec:
    """Return a stack by key, raising :class:`KeyError` if unknown."""
    try:
        return _CATALOG[key]
    except KeyError as exc:
        raise KeyError(f"unknown stack: {key!r}") from exc


def stack_keys() -> list[str]:
    """Return the sorted list of available stack keys."""
    return sorted(_CATALOG)
