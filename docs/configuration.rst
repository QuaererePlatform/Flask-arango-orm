Configuration Options
=====================

All configuration options are to be specified in the Flask app's config.

Configuration values can also be loaded from environment variables using the
:class:`flask_arango_orm.config.ArangoSettings` helper.  The
:ref:`create_app` example in the README demonstrates using
``ArangoSettings.from_env`` to populate the extension's configuration.


.. py:attribute:: ARANGODB_DATABASE
   str

   Used to specify the database name used to connect to arangodb


.. py:attribute:: ARANGODB_USER
   str

   Used to specify username used to connect to arangodb

.. py:attribute:: ARANGODB_PASSWORD
   str

   Used to specify password used to connect to arangodb

.. py:attribute:: ARANGODB_HOST
   tuple

   Default is ('http', '127.0.0.1', 8529)

   A tuple in the format of *protocol*, *host*, *port*
   Used for connecting to the arangodb host

.. py:attribute:: ARANGODB_CLUSTER
   bool

   Default is *False*

   Used to determine if connecting to a pool of hosts


.. py:attribute:: ARANGODB_HOST_POOL
   list

   A list of tuples in the format of *protocol*, *host*, *port*
   Used for connecting to a pool of arangodb hosts
