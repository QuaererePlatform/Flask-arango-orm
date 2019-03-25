"""Main module for flask_arango_orm"""
__all__ = ['ArangoORM']

from arango import ArangoClient
from arango_orm import ConnectionPool, Database
from flask import current_app, _app_ctx_stack

ARANGODB_CLUSTER = False
ARANGODB_HOST = ('http', '127.0.0.1', 8529)


class ArangoORM():
    """Flask extension for integrating the arango_orm package"""

    def __init__(self, app=None):
        """Constructor

        If a flask app instance is passed as an argument,
        :any:`init_app` is run as well.

        :param app: Flask app instance
        :type app: flask.Flask
        """
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initializes ArangoORM for use with the passed app instance

        Sets up the following defaults:

        * ARANGODB_CLUSTER = False
        * ARANGODB_HOST = ('http', '127.0.0.1', 8529)

        This should be useful for most development setups

        :param app: Flask app instance
        :type app: flask.Flask
        :return:
        """
        app.config.setdefault('ARANGODB_CLUSTER', ARANGODB_CLUSTER)
        app.config.setdefault('ARANGODB_HOST', ARANGODB_HOST)

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

        :returns: Connection to arangodb
        :rtype: arango_orm.Database
        """
        db_name = current_app.config['ARANGODB_DATABASE']
        username = current_app.config['ARANGODB_USER']
        password = current_app.config['ARANGODB_PASSWORD']

        if current_app.config['ARANGODB_CLUSTER'] == True:
            hosts = []
            host_pool = current_app.config['ARANGODB_HOST_POOL']
            for protocol, host, port in host_pool:
                hosts.append(ArangoClient(protocol=protocol,
                                          host=host,
                                          port=port))
            return ConnectionPool(hosts,
                                  dbname=db_name,
                                  password=password,
                                  username=username)
        else:
            protocol, host, port = current_app.config['ARANGODB_HOST']
            client = ArangoClient(protocol=protocol,
                                  host=host,
                                  port=port)
            return Database(client.db(name=db_name,
                                      username=username,
                                      password=password))

    @property
    def connection(self):
        """Property for storing and retrieving the database connection

        Stores the database connection in the top of the Flask
        application context stack, :any:`flask._app_ctx_stack`.  If a
        connection does not currently exist, :py:func:`connect` is
        called.

        :returns: ArangoDB connection
        :rtype: arango_orm.Database
        """
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'arangodb'):
                setattr(ctx, 'arangodb', self.connect())
                # ctx.arangodb = self.connect()
            return ctx.arangodb
