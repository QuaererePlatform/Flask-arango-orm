try:
    from unittest import mock
except ImportError:
    import mock

import flask
import pytest

from flask_arango_orm import ArangoORM


@pytest.fixture
def app():
    app = flask.Flask(__name__)
    app.config.update(
        ARANGODB_DATABASE='db',
        ARANGODB_USER='user',
        ARANGODB_PASSWORD='pass',
        ARANGODB_HOST=('http', 'localhost', 8529),
        ARANGODB_CLUSTER=False,
    )
    return app


@mock.patch('flask_arango_orm.arango.ConnectionPool')
@mock.patch('flask_arango_orm.arango.ArangoClient')
def test_connect_single_host(mock_client_cls, mock_pool_cls, app):
    arango = ArangoORM(app)

    mock_client = mock.Mock()
    mock_client_cls.return_value = mock_client
    pool = mock_pool_cls.return_value

    with app.app_context():
        conn = arango.connect()

    assert conn is pool
    mock_client_cls.assert_called_once_with(hosts='http://localhost:8529')
    mock_pool_cls.assert_called_once_with(
        [mock_client], dbname='db', username='user', password='pass'
    )


@mock.patch('flask_arango_orm.arango.ConnectionPool')
@mock.patch('flask_arango_orm.arango.ArangoClient')
def test_connect_cluster(mock_client_cls, mock_pool_cls, app):
    app.config['ARANGODB_CLUSTER'] = True
    app.config['ARANGODB_HOST_POOL'] = [
        ('http', 'host1', 8529),
        ('http', 'host2', 8529),
    ]
    arango = ArangoORM(app)

    client1 = mock.Mock(name='client1')
    client2 = mock.Mock(name='client2')
    mock_client_cls.side_effect = [client1, client2]
    pool = mock_pool_cls.return_value

    with app.app_context():
        conn = arango.connect()

    assert conn is pool
    mock_client_cls.assert_has_calls([
        mock.call(hosts='http://host1:8529'),
        mock.call(hosts='http://host2:8529'),
    ])
    mock_pool_cls.assert_called_once_with(
        [client1, client2], dbname='db', username='user', password='pass'
    )


def test_teardown_closes_connection(app):
    arango = ArangoORM(app)
    dummy_conn = mock.Mock()
    with app.app_context():
        flask.current_app.extensions['arango'] = dummy_conn
        arango.teardown()
        assert flask.current_app.extensions.get('arango') is None
    dummy_conn.close.assert_called_once()
