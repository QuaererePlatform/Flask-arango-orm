__all__ = ['ArangoORM']

from arango import ArangoClient
from arango_orm import ConnectionPool, Database
from flask import current_app, _app_ctx_stack

ARANGODB_CLUSTER = False
ARANGODB_HOST = ('http', '127.0.0.1', 8529)


class ArangoORM():
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('ARANGODB_CLUSTER', ARANGODB_CLUSTER)
        app.config.setdefault('ARANGODB_HOST', ARANGODB_HOST)

    def connect(self):
        db_name = current_app.config['ARANGODB_DATABASE']
        username = current_app.config['ARANGODB_USER']
        password = current_app.config['ARANGODB_PASSWORD']

        if current_app.config['ARANGODB_CLUSTER']:
            clients = []
            host_pool = current_app.config['ARANGODB_HOST_POOL']
            for protocol, host, port in host_pool:
                clients.append(ArangoClient(protocol=protocol,
                                            host=host,
                                            port=port))
            return ConnectionPool(clients,
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
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'arangodb'):
                ctx.arangodb = self.connect()
            return ctx.arangodb
