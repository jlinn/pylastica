.. _indexing_documents:

Indexing Documents
==================

Creating an Index
-----------------

.. code-block:: python

    # instantiate the index object
    pylastica_index = pylastica_client.get_index('index_name')

    # create the index
    pylastica_index.create({
        'number_of_shards': 4,
        'number_of_replicas': 1,
        'analysis': {
            'analyzer': {
                'indexAnalyzer': {
                    'type': 'custom',
                    'tokenizer': 'standard',
                    'filter': ['lowercase', 'mySnowball']
                }
            }
        },
        'filter': {
            'mySnowball': {
                'type': 'snowball',
                'language': 'English'
            }
        }
    },
    True
    )

Defining a Mapping
------------------

.. code-block:: python

    # create a DocType object
    doc_type = pylastica_index.get_doc_type('type_name')

    # define the mapping
    mapping = pylastica.doc_type.Mapping()
    mapping.doc_type = doc_type
    mapping.set_param('index_analyzer', 'indexAnalyzer')

    # define boost field
    mapping.set_param('_boost', {'name': '_boost', 'null_value': 1.0})

    mapping.set_properties({
        'id': {'type': 'integer', 'include_in_all': False},
        'user': {
            'type': 'object',
            'properties': {
                'name': {'type': 'string', 'include_in_all': True},
                'fullName': {'type': 'string', 'include_in_all': True}
            }
        },
        '_boost': {'type': 'float', 'include_in_all': False}
    })

    # send the mapping to Elasticsearch
    mapping.send()

Adding Documents
----------------

.. code-block:: python

    # the id of the dicument
    id = 1

    # create a document
    document = pylastica.Document(id, {
        'id': id,
        'user': {
            'name': 'Neo',
            'fullName': 'Thomas Anderson'
        },
        '_boost': 1.0
    })

    # index the document
    doc_type.add_document(document)

Elasticsearch indices are typically configured to refresh automatically. However, if you need the document which you have just indexed to be available immediately, it may be necessary to manually refresh the index:

.. code-block:: python

    doc_type.index.refresh()

Bulk Indexing
-------------

.. code-block:: python

    # define documents
    documents = [
        pylastica.Document(1, {...})
        pylastica.Document(2, {...})
    ]

    doc_type.add_documents(documents)

