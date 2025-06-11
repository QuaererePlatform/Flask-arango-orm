"""Main module for flask_arango_orm"""
__all__ = ['ArangoORM']

from arango import ArangoClient
from arango_orm.connection_pool import ConnectionPool
from flask import current_app, Flask

ARANGODB_CLUSTER = False
ARANGODB_HOST = ('http', '127.0.0.1', 8529)


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
        self.app.config.setdefault('ARANGODB_CLUSTER', ARANGODB_CLUSTER)
        self.app.config.setdefault('ARANGODB_HOST', ARANGODB_HOST)
        if not hasattr(self.app, 'extensions'):
            self.app.extensions = {}
        self.app.extensions.setdefault('arango', None)
        self.app.teardown_appcontext(self.teardown)

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

        :returns: Connection pool for ArangoDB
        :rtype: arango_orm.connection_pool.ConnectionPool
        """
        db_name = current_app.config['ARANGODB_DATABASE']
        username = current_app.config['ARANGODB_USER']
        password = current_app.config['ARANGODB_PASSWORD']

        hosts = []
        if current_app.config['ARANGODB_CLUSTER']:
            host_pool = current_app.config['ARANGODB_HOST_POOL']
        else:
            host_pool = [current_app.config['ARANGODB_HOST']]

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

        return ConnectionPool(
            hosts,
            dbname=db_name,
            password=password,
            username=username,
        )

    @property
    def connection(self):
        """Property for storing and retrieving the database connection

        Stores the database connection in the top of the Flask
        application context stack, :any:`flask._app_ctx_stack`.  If a
        connection does not currently exist, :py:func:`connect` is
        called.

        :returns: Connection pool instance
        :rtype: arango_orm.connection_pool.ConnectionPool
        """
        if current_app.extensions.get('arango') is None:
            current_app.extensions['arango'] = self.connect()
        return current_app.extensions['arango']

    def teardown(self, exception=None):
        conn = current_app.extensions.pop('arango', None)
        if conn is not None and hasattr(conn, 'close'):
            conn.close()
