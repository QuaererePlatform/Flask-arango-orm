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
