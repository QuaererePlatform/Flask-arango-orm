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
``create_app`` factory can load configuration from environment variables using
the :class:`~flask_arango_orm.config.ArangoSettings` helper:

.. code-block:: python

   from flask import Flask
   from flask_arango_orm import ArangoORM, ArangoSettings

   def create_app() -> Flask:
       app = Flask(__name__)

       settings = ArangoSettings.from_env()
       app.config.update(
           ARANGODB_DATABASE=settings.database,
           ARANGODB_USER=settings.user,
           ARANGODB_PASSWORD=settings.password,
           ARANGODB_HOST=settings.host,
           ARANGODB_CLUSTER=settings.cluster,
           ARANGODB_HOST_POOL=settings.host_pool,
       )

       arango = ArangoORM(app)

      @app.route('/route')
      def some_route():
          # ``db_conn`` is an ``arango_orm.database.Database`` instance
          db_conn = arango.connection
          return 'ok'

       return app

Connecting to ArangoDB clusters
-------------------------------

To work with an ArangoDB cluster enable ``ARANGODB_CLUSTER`` and provide
``ARANGODB_HOST_POOL`` with the coordinator URLs. The extension uses
``python-arango``'s ``ArangoClient`` to create a connection pool.  The
``connection`` property returns the next ``Database`` instance from this
pool.

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

Async usage
-----------

``AsyncArangoORM`` works the same way when writing async routes. Retrieve the
connection with ``await``:

.. code-block:: python

   from flask import Flask
   from flask_arango_orm import AsyncArangoORM

   app = Flask(__name__)
   arango = AsyncArangoORM(app)

   @app.get("/async")
   async def async_route():
       db = await arango.connection()
       return "ok"

Logging
-------

``flask_arango_orm`` uses the standard :mod:`logging` package. The
``flask_arango_orm.arango`` module exposes a logger named after the module,
which reports connection attempts, successful connections and when connections
are torn down.  Enable it with::

   import logging
   logging.basicConfig(level=logging.INFO)


