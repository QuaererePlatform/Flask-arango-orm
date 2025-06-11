from unittest import mock

import flask
import pytest

from flask_arango_orm import AsyncArangoORM
from flask_arango_orm.arango import ARANGODB_CLUSTER, ARANGODB_HOST


class TestAsyncArangoORM:
    @mock.patch("flask.Flask")
    def test_init(self, mock_flask):
        app = mock_flask(__name__)
        _ = AsyncArangoORM(app)
        calls = [
            mock.call("ARANGODB_CLUSTER", ARANGODB_CLUSTER),
            mock.call("ARANGODB_HOST", ARANGODB_HOST),
        ]
        app.config.setdefault.assert_has_calls(calls)

    def test_init_no_app(self):
        arango = AsyncArangoORM()
        assert arango.app is None

    @pytest.mark.asyncio
    @mock.patch.object(AsyncArangoORM, "connect", new_callable=mock.AsyncMock)
    async def test_connection_attribute(self, mock_connect):
        test_conn = object()
        mock_client = mock.AsyncMock()
        mock_connect.return_value = (mock_client, test_conn)

        app = flask.Flask(__name__)
        arango = AsyncArangoORM(app)
        ctx = app.app_context()
        ctx.push()
        app.do_teardown_appcontext = lambda exc=None: None
        db_conn = await arango.connection()
        assert db_conn is test_conn
        assert app.extensions["arango_async"] == (mock_client, test_conn)
        await arango.teardown()
        mock_connect.assert_awaited_once()
