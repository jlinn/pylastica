.. _installation:

Installation
============

Requirements
------------

Pylastica requires python v2.7, the urllib3 package, and the dateutils package. For thrift functionality, the thrift package is required, as well.

Installing
----------

.. code-block:: bash

    $ pip install pylastica

The urllib3 and dateutils packages will be installed automatically. If you wish to use the thrift transport client, the thrift module must be installed manually:

.. code-block:: bash

    $ pip install thrift

Connecting to Elasticsearch
---------------------------

Assuming one Elasticsearch node running locally on port 9200:

.. code-block:: python

    import pylastica

    pylastica_client = pylastica.Client('localhost', 9200)

To connect to multiple nodes:

.. code-block:: python

    import pylastica

    pylastica_client = pylastica.Client(connections=[
        {'host': 'localhost', 'port': 9200},
        {'host': 'localhost', 'port': 9201}
    ])