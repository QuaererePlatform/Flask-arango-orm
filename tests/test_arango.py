try:
    from unittest import mock
except ImportError:
    import mock

from flask import Flask
from flask_arango_orm import ArangoORM
from flask_arango_orm.arango import ARANGODB_HOST
from arango_orm import Collection


class Car(Collection):
    __collection__ = "cars"


class TestArangoORM:

    '''
    @mock.patch('flask.Flask')
    def test_init(self, mock_flask):
        app = mock_flask(__name__)
        _ = ArangoORM(app)
        calls = [mock.call('ARANGODB_CLUSTER', ARANGODB_CLUSTER),
                 mock.call('ARANGODB_HOST', ARANGODB_HOST)]
        app.config.setdefault.assert_has_calls(calls)
    '''
    '''
    def test_init_no_app(self):
        arango = ArangoORM()
        assert arango.app is None
    '''

    # @mock.patch('flask_arango_orm.arango.Database')
    # @mock.patch('flask_arango_orm.arango.ArangoClient')
    # @mock.patch('flask_arango_orm.arango.ArangoClient.app')
    def test_connect_single(self):
        app = Flask(__name__)
        arango_db = 'test_db'
        arango_user = 'test_user'
        arango_passwd = 'test_password'
        # app.config = {}
        app.config['SERVER_NAME'] = "localhost"
        app.config['ARANGODB_DATABASE'] = arango_db
        app.config['ARANGODB_USER'] = arango_user
        app.config['ARANGODB_PASSWORD'] = arango_passwd
        app.config['ARANGODB_CLUSTER'] = False
        app.config['ARANGODB_HOST'] = ARANGODB_HOST
        arango = ArangoORM(app)
        arango.init_app(app)
        with app.app_context():
            try:
                db = arango.connect()
                if db.has_collection(Car) is False:
                    db.create_collection(Car)
                db.has_collection(Car)
            except Exception as e:
                assert False, e
        '''
        protocol, host, port = ARANGODB_HOST
        mock_client.assert_called_with(
            hosts="{protocol}://{host}:{port}".format(
                protocol=protocol,
                host=host,
                port=port
            )
        )
        '''

        '''
        mock_db.assert_called_with(
            mock_client.return_value.db(name=arango_db,
                                        username=arango_user,
                                        password=arango_passwd))
        '''

    @mock.patch('flask_arango_orm.arango.ConnectionPool')
    @mock.patch('flask_arango_orm.arango.ArangoClient')
    # @mock.patch('flask_arango_orm.arango.current_app')
    def test_connect_cluster(self, mock_client, mock_pool):
        app = Flask(__name__)
        arango_db = 'test_db'
        arango_user = 'test_user'
        arango_passwd = 'test_password'
        host_pool = [('http', '127.0.0.1', 8529),
                     ('http', '127.0.0.2', 8530),
                     ('https', '127.0.0.3', 8529)]
        hosts = [
            "{protocol}://{host}:{port}".format(
                protocol=protocol,
                host=host,
                port=port
            ) for protocol, host, port in host_pool
        ]

        app.config['ARANGODB_DATABASE'] = arango_db
        app.config['ARANGODB_USER'] = arango_user
        app.config['ARANGODB_PASSWORD'] = arango_passwd
        app.config['ARANGODB_CLUSTER'] = True
        app.config['ARANGODB_HOST_POOL'] = host_pool
        arango = ArangoORM(app)
        with app.app_context():
            arango.connect()
        calls = [mock.call(hosts=h) for h in hosts]
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
        with app.app_context():
            db_conn = arango.connection
            assert db_conn == test_conn
