pylastica: elasticsearch python client
======================================

.. image:: https://secure.travis-ci.org/jlinn/pylastica.png?branch=master
        :target: http://travis-ci.org/jlinn/pylastica

About
-----

Pylastica is a Python port of `Elastica <https://github.com/ruflin/Elastica>`_, a PHP `Elasticsearch <http://www.elasticsearch.org/>`_ client
by `Nicolas Ruflin <https://github.com/ruflin>`_.

Installation
------------

.. code-block:: bash

    $ pip install pylastica


To use the thrift transport protocol, you will need to install the `thrift transport plugin <https://github.com/elasticsearch/elasticsearch-transport-thrift>`_.

To index attachments, you will need to install the `mapper attachments plugin <https://github.com/elasticsearch/elasticsearch-mapper-attachments>`_.

To use a RabbitMQ river, you will need to install the `RabbitMQ river plugin <https://github.com/elasticsearch/elasticsearch-river-rabbitmq/blob/master/README.md>`_.


Documentation
-------------

Documentation can be found `here <https://pylastica.readthedocs.org>`_.

Compatibility
-------------

Pylastica is tested with Python 2.7 and Elasticsearch version 1.2.1.

Changes
-------

See the `changelog <https://github.com/jlinn/pylastica/blob/master/changes.markdown>`_.