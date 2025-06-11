from importlib.metadata import PackageNotFoundError, version

from .arango import ArangoORM

try:
    __version__ = version("Flask-arango-orm")
except PackageNotFoundError:  # pragma: no cover - package not installed
    __version__ = "0.0.0"

__all__ = (
    "ArangoORM",
    "__version__",
)
