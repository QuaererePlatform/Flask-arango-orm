"""Main module for flask_arango_orm"""

__all__ = ["ArangoORM", "AsyncArangoORM"]

from arango import ArangoClient
from arango_orm.connection_pool import ConnectionPool
from flask import current_app, Flask
from aioarango import ArangoClient as AsyncArangoClient

from .config import ArangoSettings

ARANGODB_CLUSTER = False
ARANGODB_HOST = ("http", "127.0.0.1", 8529)


class ArangoORM:
    """Flask extension for integrating the arango_orm package"""

    def __init__(self, app: Flask = None):
        """Constructor

        If a flask app instance is passed as an argument,
        :any:`init_app` is run as well.

        :param app: Flask app instance
        :type app: flask.Flask
        """
        self.app = app
        self.settings: ArangoSettings | None = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        """Initializes ArangoORM for use with the passed app instance

        Sets up the following defaults:

        * ARANGODB_CLUSTER = False
        * ARANGODB_HOST = ('http', '127.0.0.1', 8529)

        This should be useful for most development setups

        :param app: Flask app instance
        :type app: flask.Flask
        :return:
        """
        if self.app is None:
            self.app = app
        self.app.config.setdefault("ARANGODB_CLUSTER", ARANGODB_CLUSTER)
        self.app.config.setdefault("ARANGODB_HOST", ARANGODB_HOST)
        if not hasattr(self.app, "extensions"):
            self.app.extensions = {}
        self.app.extensions.setdefault("arango", None)
        self.app.teardown_appcontext(self.teardown)

        self.settings = ArangoSettings.from_mapping(self.app.config)

    def connect(self):
        """Sets up the connection to the arangodb database

        Uses app configuration for setup, utilizing the following:

        * ARANGODB_DATABASE
        * ARANGODB_USER
        * ARANGODB_PASSWORD
        * ARANGODB_HOST
        * ARANGODB_CLUSTER
        * ARANGODB_HOST_POOL

        If ARANGODB_CLUSTER is True, then the host configuration is
        taken from ARANGODB_HOST_POOL, otherwise ARANGODB_HOST is used.

        :returns: Database connection
        :rtype: arango_orm.database.Database
        """
        settings = self.settings or ArangoSettings.from_mapping(current_app.config)

        db_name = settings.database
        username = settings.user
        password = settings.password

        hosts = []
        if settings.cluster:
            host_pool = settings.host_pool
        else:
            host_pool = [settings.host]

        for protocol, host, port in host_pool:
            hosts.append(
                ArangoClient(
                    hosts="{protocol}://{host}:{port}".format(
                        protocol=protocol,
                        host=host,
                        port=port,
                    )
                )
            )

        pool = ConnectionPool(
            hosts,
            dbname=db_name,
            password=password,
            username=username,
        )
        return pool._db

    @property
    def connection(self):
        """Property for storing and retrieving the database connection

        Stores the database connection in the top of the Flask
        application context stack, :any:`flask._app_ctx_stack`.  If a
        connection does not currently exist, :py:func:`connect` is
        called.

        :returns: Database instance
        :rtype: arango_orm.database.Database
        """
        if current_app.extensions.get("arango") is None:
            current_app.extensions["arango"] = self.connect()
        return current_app.extensions["arango"]

    def teardown(self, exception=None):
        conn = current_app.extensions.pop("arango", None)
        if conn is not None and hasattr(conn, "close"):
            conn.close()


class AsyncArangoORM:
    """Asynchronous version of :class:`ArangoORM` using ``aioarango``."""

    def __init__(self, app: Flask | None = None) -> None:
        self.app = app
        self.settings: ArangoSettings | None = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        if self.app is None:
            self.app = app
        self.app.config.setdefault("ARANGODB_CLUSTER", ARANGODB_CLUSTER)
        self.app.config.setdefault("ARANGODB_HOST", ARANGODB_HOST)
        if not hasattr(self.app, "extensions"):
            self.app.extensions = {}
        self.app.extensions.setdefault("arango_async", None)
        self.app.teardown_appcontext(self.teardown)

        self.settings = ArangoSettings.from_mapping(self.app.config)

    async def connect(self):
        settings = self.settings or ArangoSettings.from_mapping(current_app.config)

        db_name = settings.database
        username = settings.user
        password = settings.password

        if settings.cluster:
            host_pool = settings.host_pool
        else:
            host_pool = [settings.host]

        hosts = [f"{proto}://{host}:{port}" for proto, host, port in host_pool]

        client = AsyncArangoClient(hosts=hosts)
        db = await client.db(db_name, username, password)
        return client, db

    async def connection(self):
        if current_app.extensions.get("arango_async") is None:
            current_app.extensions["arango_async"] = await self.connect()
        _, db = current_app.extensions["arango_async"]
        return db

    async def teardown(self, exception: Exception | None = None) -> None:
        conn = current_app.extensions.pop("arango_async", None)
        if conn is not None:
            client, _ = conn
            await client.close()
