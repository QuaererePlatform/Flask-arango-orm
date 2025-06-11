Cluster Connections
===================

Flask-arango-orm can connect to an ArangoDB cluster using
`python-arango`_. Enable ``ARANGODB_CLUSTER`` and provide
``ARANGODB_HOST_POOL`` with the coordinator hosts.

.. code-block:: python

   from flask import Flask
   from flask_arango_orm import ArangoORM

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

For more details on cluster connection handling see the
`python-arango documentation <https://python-arango.readthedocs.io/>`_.
