from importlib.metadata import PackageNotFoundError, version

from .arango import ArangoORM, AsyncArangoORM
from .config import ArangoSettings

try:
    __version__ = version("Flask-arango-orm")
except PackageNotFoundError:  # pragma: no cover - package not installed
    __version__ = "0.0.0"

__all__ = (
    "ArangoORM",
    "AsyncArangoORM",
    "ArangoSettings",
    "__version__",
)
