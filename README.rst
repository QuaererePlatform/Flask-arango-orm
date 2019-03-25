About
-----

Flask-arango-orm is used to connect to an `ArangoDB`_ instance using `arango-orm`_ as an object
model layer to your `Flask`_ app.  ArangoDB is a hybrid database that can provide a document, graph,
and relational mode which can be taken advantage of using arango-orm.

.. _ArangoDB: https://www.arangodb.com/
.. _arango-orm: https://github.com/threatify/arango-orm
.. _Flask: http://flask.pocoo.org/docs/1.0/

Installation
------------

Using pip:

.. code-block:: shell

   pip install Flask-arango-orm

Or using setup.py:

.. code-block:: shell

   python setup.py install


Tests can be ran using:

.. code-block:: shell

   python setup.py test


Documentation can be generated using:

.. code-block:: shell

   python setup.py build_sphinx


Usage
-----

This extension for the Flask framework uses arango-orm to provide an Object Model to use
within the Flask application.

.. code-block:: python

   from flask import Flask
   from flask_arango_orm import ArangoORM

   app = Flask(__name__)
   arango = ArangoORM(app)

   @app.route('/route')
   def some_route():
      db_conn = arango.connection

