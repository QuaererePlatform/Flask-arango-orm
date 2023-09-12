try:
    from unittest import mock
except ImportError:
    import mock

from flask_arango_orm import ArangoORM
from flask_arango_orm.arango import ARANGODB_CLUSTER, ARANGODB_HOST


class TestArangoORM:

    @mock.patch('flask.Flask')
    def test_init(self, mock_flask):
        app = mock_flask(__name__)
        _ = ArangoORM(app)
        calls = [mock.call('ARANGODB_CLUSTER', ARANGODB_CLUSTER),
                 mock.call('ARANGODB_HOST', ARANGODB_HOST)]
        app.config.setdefault.assert_has_calls(calls)

    def test_init_no_app(self):
        arango = ArangoORM()
        assert arango.app is None

    @mock.patch('flask_arango_orm.arango.Database')
    @mock.patch('flask_arango_orm.arango.ArangoClient')
    @mock.patch('flask_arango_orm.arango.current_app')
    def test_connect_single(self, mock_current_app, mock_client, mock_db):
        arango_db = 'test_db'
        arango_user = 'test_user'
        arango_passwd = 'test_password'
        mock_current_app.config = {}
        mock_current_app.config['ARANGODB_DATABASE'] = arango_db
        mock_current_app.config['ARANGODB_USER'] = arango_user
        mock_current_app.config['ARANGODB_PASSWORD'] = arango_passwd
        mock_current_app.config['ARANGODB_CLUSTER'] = False
        mock_current_app.config['ARANGODB_HOST'] = ARANGODB_HOST
        arango = ArangoORM()
        arango.connect()
        protocol, host, port = ARANGODB_HOST
        mock_client.assert_called_with(protocol=protocol,
                                       host=host,
                                       port=port)
        mock_db.assert_called_with(
            mock_client.return_value.db(name=arango_db,
                                        username=arango_user,
                                        password=arango_passwd))

    @mock.patch('flask_arango_orm.arango.ConnectionPool')
    @mock.patch('flask_arango_orm.arango.ArangoClient')
    @mock.patch('flask_arango_orm.arango.current_app')
    def test_connect_cluster(self, mock_current_app, mock_client, mock_pool):
        arango_db = 'test_db'
        arango_user = 'test_user'
        arango_passwd = 'test_password'
        host_pool = [('http', '127.0.0.1', 8529),
                     ('http', '127.0.0.2', 8530),
                     ('https', '127.0.0.3', 8529)]
        mock_current_app.config = {}
        mock_current_app.config['ARANGODB_DATABASE'] = arango_db
        mock_current_app.config['ARANGODB_USER'] = arango_user
        mock_current_app.config['ARANGODB_PASSWORD'] = arango_passwd
        mock_current_app.config['ARANGODB_CLUSTER'] = True
        mock_current_app.config['ARANGODB_HOST_POOL'] = host_pool
        arango = ArangoORM()
        arango.connect()
        calls = [mock.call(protocol=protocol,
                           host=host,
                           port=port) for protocol, host, port in host_pool]
        mock_client.assert_has_calls(calls)
        # TODO: Need to figure out ConnectionPool arguments
        mock_pool.assert_called_once()

    @mock.patch.object(ArangoORM, 'connect')
    def test_connection_attribute(self, mock_connect):
        test_conn = 'Test DB connection'
        mock_connect.return_value = test_conn

        import flask
        app = flask.Flask(__name__)
        arango = ArangoORM(app)
        with app.test_request_context():
            db_conn = arango.connection
            assert db_conn == test_conn
