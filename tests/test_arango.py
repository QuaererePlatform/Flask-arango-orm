from unittest import mock

from flask_arango_orm import ArangoORM
from flask_arango_orm.arango import ARANGODB_CLUSTER, ARANGODB_HOST


class TestArangoORM:
    @mock.patch("flask.Flask")
    def test_init(self, mock_flask):
        app = mock_flask(__name__)
        _ = ArangoORM(app)
        calls = [
            mock.call("ARANGODB_CLUSTER", ARANGODB_CLUSTER),
            mock.call("ARANGODB_HOST", ARANGODB_HOST),
        ]
        app.config.setdefault.assert_has_calls(calls)

    def test_init_no_app(self):
        arango = ArangoORM()
        assert arango.app is None

    @mock.patch.object(ArangoORM, "connect")
    def test_connection_attribute(self, mock_connect):
        class DummyConn:
            def __init__(self):
                self.closed = False

            def close(self):
                self.closed = True

        test_conn = DummyConn()
        mock_connect.return_value = test_conn

        import flask

        app = flask.Flask(__name__)
        arango = ArangoORM(app)
        with app.test_request_context():
            db_conn = arango.connection
            assert db_conn is test_conn
            assert app.extensions["arango"] is test_conn
        assert test_conn.closed

    @mock.patch.object(ArangoORM, "connect")
    def test_connection_repeated_use(self, mock_connect):
        import flask

        db_obj = object()
        mock_connect.return_value = db_obj

        app = flask.Flask(__name__)
        arango = ArangoORM(app)

        with app.test_request_context():
            first = arango.connection
            second = arango.connection

            assert first is second
            assert app.extensions["arango"] is db_obj
        mock_connect.assert_called_once()
