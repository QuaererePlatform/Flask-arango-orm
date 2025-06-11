About
-----

Flask-arango-orm is used to connect to an `ArangoDB`_ instance using `arango-orm`_ as an object
model layer to your `Flask`_ app.  ArangoDB is a hybrid database that can provide a document, graph,
and relational mode which can be taken advantage of using arango-orm.

.. _ArangoDB: https://www.arangodb.com/
.. _arango-orm: https://github.com/threatify/arango-orm
.. _Flask: https://flask.palletsprojects.com/

Installation
------------

Using pip:

.. code-block:: shell

   pip install Flask-arango-orm

Using Poetry:

.. code-block:: shell

   poetry add Flask-arango-orm


Tests can be ran using:

.. code-block:: shell

   poetry run pytest


Documentation can be generated using:

.. code-block:: shell

   make -C docs html


Usage
-----

The extension integrates `arango-orm` with your Flask application. A modern
``create_app`` factory can load configuration from environment variables:

.. code-block:: python

   import os
   from urllib.parse import urlparse
   from flask import Flask
   from flask_arango_orm import ArangoORM

   def create_app() -> Flask:
       app = Flask(__name__)

       app.config['ARANGODB_DATABASE'] = os.getenv('ARANGODB_DATABASE', 'test')
       app.config['ARANGODB_USER'] = os.getenv('ARANGODB_USER', 'root')
       app.config['ARANGODB_PASSWORD'] = os.getenv('ARANGODB_PASSWORD', '')

       host = urlparse(os.getenv('ARANGODB_HOST', 'http://127.0.0.1:8529'))
       app.config['ARANGODB_HOST'] = (host.scheme, host.hostname, host.port)

       arango = ArangoORM(app)

       @app.route('/route')
       def some_route():
           db_conn = arango.connection
           return 'ok'

       return app

Connecting to ArangoDB clusters
-------------------------------

To work with an ArangoDB cluster enable ``ARANGODB_CLUSTER`` and provide
``ARANGODB_HOST_POOL`` with the coordinator URLs. The extension uses
``python-arango``'s ``ArangoClient`` to create a connection pool.

.. code-block:: python

   def create_app() -> Flask:
       app = Flask(__name__)

       pool = [
           ('http', 'coordinator1', 8529),
           ('http', 'coordinator2', 8529),
       ]
       app.config.update(
           ARANGODB_CLUSTER=True,
           ARANGODB_HOST_POOL=pool,
       )

       ArangoORM(app)
       return app

