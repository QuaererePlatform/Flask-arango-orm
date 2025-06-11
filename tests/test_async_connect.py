from unittest import mock

import flask
import pytest

from flask_arango_orm import AsyncArangoORM


@pytest.fixture
def app():
    app = flask.Flask(__name__)
    app.config.update(
        ARANGODB_DATABASE="db",
        ARANGODB_USER="user",
        ARANGODB_PASSWORD="pass",
        ARANGODB_HOST=("http", "localhost", 8529),
        ARANGODB_CLUSTER=False,
    )
    return app


@pytest.mark.asyncio
@mock.patch("flask_arango_orm.arango.AsyncArangoClient")
async def test_connect_single_host(mock_client_cls, app):
    arango = AsyncArangoORM(app)

    mock_client = mock.AsyncMock()
    mock_db = mock.AsyncMock()
    mock_client.db.return_value = mock_db
    mock_client_cls.return_value = mock_client

    ctx = app.app_context()
    ctx.push()
    app.do_teardown_appcontext = lambda exc=None: None
    client, db = await arango.connect()
    await arango.teardown()

    assert db is mock_db
    mock_client_cls.assert_called_once_with(hosts=["http://localhost:8529"])
    mock_client.db.assert_awaited_once_with("db", "user", "pass")


@pytest.mark.asyncio
@mock.patch("flask_arango_orm.arango.AsyncArangoClient")
async def test_connect_cluster(mock_client_cls, app):
    app.config["ARANGODB_CLUSTER"] = True
    app.config["ARANGODB_HOST_POOL"] = [
        ("http", "host1", 8529),
        ("http", "host2", 8529),
    ]
    arango = AsyncArangoORM(app)

    mock_client = mock.AsyncMock()
    mock_db = mock.AsyncMock()
    mock_client.db.return_value = mock_db
    mock_client_cls.return_value = mock_client

    ctx = app.app_context()
    ctx.push()
    app.do_teardown_appcontext = lambda exc=None: None
    client, db = await arango.connect()
    await arango.teardown()

    assert db is mock_db
    mock_client_cls.assert_called_once_with(
        hosts=["http://host1:8529", "http://host2:8529"]
    )
    mock_client.db.assert_awaited_once_with("db", "user", "pass")


@pytest.mark.asyncio
async def test_teardown_closes_connection(app):
    arango = AsyncArangoORM(app)
    dummy_client = mock.AsyncMock()
    dummy_db = mock.Mock()
    ctx = app.app_context()
    ctx.push()
    flask.current_app.extensions["arango_async"] = (dummy_client, dummy_db)
    await arango.teardown()
    assert flask.current_app.extensions.get("arango_async") is None
    dummy_client.close.assert_awaited_once()
