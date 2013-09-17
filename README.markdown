pylastica: elasticsearch python client
======================================
[![Build Status](https://secure.travis-ci.org/jlinn/pylastica.png?branch=master)](http://travis-ci.org/jlinn/pylastica)

About
-----
Pylastica is a Python port of [Elastica](https://github.com/ruflin/Elastica), a PHP [Elasticsearch](http://www.elasticsearch.org/) client
by [Nicolas Ruflin](https://github.com/ruflin).

Installation
------------
```
pip install pylastica
```

To use the thrift transport protocol, you will need to install the [thrift transport plugin](https://github.com/elasticsearch/elasticsearch-transport-thrift).

To index attachments, you will need to install the [mapper attachments plugin](https://github.com/elasticsearch/elasticsearch-mapper-attachments).

To use a RabbitMQ river, you will need to install the [RabbitMQ river plugin](https://github.com/elasticsearch/elasticsearch-river-rabbitmq/blob/master/README.md).


Documentation
-------------
Documentation can be found [here](https://pylastica.readthedocs.org).

Compatibility
-------------
Pylastica is tested with Python 2.7 and Elasticsearch version 0.90.4.