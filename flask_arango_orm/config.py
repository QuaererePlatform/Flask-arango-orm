from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Tuple, Mapping
import os
from urllib.parse import urlparse

Host = Tuple[str, str, int]


def _parse_bool(value: str | bool | None) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).lower() in {"1", "true", "yes"}


def _parse_host(value: Host | str | None) -> Host:
    if isinstance(value, tuple):
        return value
    if value is None:
        value = "http://127.0.0.1:8529"
    parsed = urlparse(str(value))
    return (parsed.scheme or "http", parsed.hostname or "127.0.0.1", parsed.port or 8529)


def _parse_host_pool(value: List[Host] | str | None) -> List[Host]:
    if isinstance(value, list):
        return value
    hosts: List[Host] = []
    if not value:
        return hosts
    for item in str(value).split(','):
        item = item.strip()
        if item:
            hosts.append(_parse_host(item))
    return hosts


@dataclass
class ArangoSettings:
    database: str
    user: str
    password: str
    host: Host = ("http", "127.0.0.1", 8529)
    cluster: bool = False
    host_pool: List[Host] = field(default_factory=list)

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, object]) -> "ArangoSettings":
        return cls(
            database=str(mapping.get("ARANGODB_DATABASE", "")),
            user=str(mapping.get("ARANGODB_USER", "")),
            password=str(mapping.get("ARANGODB_PASSWORD", "")),
            host=_parse_host(mapping.get("ARANGODB_HOST")),
            cluster=_parse_bool(mapping.get("ARANGODB_CLUSTER")),
            host_pool=_parse_host_pool(mapping.get("ARANGODB_HOST_POOL")),
        )

    @classmethod
    def from_env(cls) -> "ArangoSettings":
        return cls.from_mapping(os.environ)
