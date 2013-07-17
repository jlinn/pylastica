__author__ = 'Joe Linn'

import urllib
#import pylastica
from .abstracttype import *
from .mapping import *

class DocType(pylastica.searchable.Searchable):
    def __init__(self, index, name):
        """
        @param index: index object
        @type index: pylastica.index.Index
        @param name: document type name
        @type name: str
        """
        assert isinstance(index, pylastica.index.Index), "index must be of type Index: %r" % index
        self._index = index
        self._name = name
        self._serializer = None

    def add_document(self, doc):
        """
        Adds the given document to the index
        @param doc:
        @type doc: pylastica.document.Document
        @return:
        @rtype: pylastica.response.Response
        """
        assert isinstance(doc, pylastica.document.Document), "doc must be of type Document: %r" % doc
        path = urllib.quote_plus(str(doc.doc_id))
        request_type = pylastica.request.Request.PUT
        if path is None or path == '':
            #no doc id has been given; use post so that an id is automatically created
            request_type = pylastica.request.Request.POST
        options = doc.get_options([
            'version',
            'version_type',
            'routing',
            'percolate',
            'parent',
            'ttl',
            'timestamp',
            'op_type',
            'consistency',
            'replication',
            'refresh',
            'timeout'
        ])
        response = self.request(path, request_type, doc.data, options)
        data = response.data
        if (doc.auto_populate or self.index.client.get_config_value(['document', 'autoPopulate'], False)) and response.is_ok():
            if doc.has_id():
                if '_id' in data:
                    doc.doc_id = data['_id']
            if '_version' in data:
                doc.version = data['_version']
        return response

    def update_document(self, data):
        """
        Update a document using an update script.
        @param doc: document with update data
        @type doc: pylastica.document.Document or pylastica.script.Script
        @return:
        @rtype: pylastica.response.Response
        """
        if not isinstance(data, pylastica.document.Document) and not isinstance(data, pylastica.script.Script):
            raise TypeError("data must be an instance of Document or Script: %r" % data)
        if not data.has_id():
            raise pylastica.exception.InvalidException("Document id is not set.")
        return self.index.client.update_document(data.doc_id, data, self.index.name, self.name)

    def add_documents(self, docs):
        """
        Use _bulk to send multiple documents to the server
        @param docs: list of doucments
        @type docs: list of pylastica.document.Document
        @return:
        @rtype: pylastica.bulk.ResponseSet
        """
        for doc in docs:
            assert isinstance(doc, pylastica.document.Document), "All items in list docs must be of type Document: %r" % doc
            doc.doc_type = self.name
        return self.index.add_documents(docs)

    def get_document(self, doc_id, options=None):
        """
        Retrieve a specific document from the index
        @param doc_id: document id
        @type doc_id: str
        @param options: options for the get request
        @type options: dict
        @return:
        @rtype: pylastica.document.Document
        """
        path = urllib.quote_plus(str(doc_id))
        try:
            result = self.request(path, pylastica.request.Request.GET, query=options).data
        except pylastica.exception.ResponseException:
            raise pylastica.exception.NotFoundException("Document with id %s not found." % doc_id)
        if result['exists'] is None or result['exists'] == '' or not result['exists']:
            raise pylastica.exception.NotFoundException("Document with id %s not found." % doc_id)
        data = result['_source'] if '_source' in result else {}
        document = pylastica.document.Document(doc_id, data, self.name, self.index)
        document.version = result['_version']
        return document

    def create_document(self, doc_id=None, data=None):
        """

        @param doc_id:
        @type doc_id: str or int
        @param data:
        @type data: dict or str
        @return:
        @rtype: pylastica.document.Document
        """
        return pylastica.document.Document(doc_id, data, doc_type=self, index=self.index)

    @property
    def name(self):
        """

        @return: type name
        @rtype: str
        """
        return self._name

    def set_mapping(self, mapping):
        """
        Sets the value type mapping
        @param mapping:
        @type mapping: pylastica.doc_type.Mapping or dict
        @return:
        @rtype: pylastica.response.Response
        """
        mapping = pylastica.doc_type.Mapping.create(mapping)
        mapping.doc_type = self
        return mapping.send()

    @property
    def mapping(self):
        """
        Returns the current mapping for this type
        @return:
        @rtype: dict
        """
        return self.request('_mapping', pylastica.request.Request.GET).data

    @mapping.setter
    def mapping(self, mapping):
        """
        Sets the value type mapping.
        @param mapping:
        @type mapping: pylastica.type.Mapping or dict
        @return:
        @rtype: pylastica.response.Response
        """
        self.set_mapping(mapping)

    def create_search(self, query=None, options=None):
        """

        @param query:
        @type query: pylastica.query.Query
        @param options:
        @type options:  dict
        @return:
        @rtype: pylastica.search.Search
        """
        search = pylastica.search.Search(self.index.client)
        return search.add_index(self.index).add_type(self).set_options_and_query(options, query)

    def search(self, query=None, options=None):
        """
        Searches results for a query
        @param query: dict with all query data or a Query object
        @type query: str or dict or pylastica.query.Query or pylastica.query.AbstractQuery
        @param options:
        @type options: dict
        @return: result set with all results
        @rtype: pylastica.resultset.ResultSet
        """
        return self.create_search(query, options).search()

    def count(self, query=None):
        """
        Counts results for a query. If no query is set, a MatchAll query is used.
        @param query: dict with all query data or a Query object
        @type query: dict or pylastica.query.Query or str
        @return: number of docs matching the query
        @rtype: int
        """
        return self.create_search(query).count()

    @property
    def index(self):
        """
        Returns the index object associated with this type
        @return:
        @rtype: pylastica.index.Index
        """
        return self._index

    def delete_document(self, document):
        """
        Delete the given document from the current index
        @param document:
        @type document: pylastica.document.Document
        @return:
        @rtype: pylastica.response.Response
        """
        assert isinstance(document, pylastica.document.Document), "document must be a Document object: %r" % document
        options = document.get_options([
            'version',
            'version_type',
            'routing',
            'parent',
            'replication',
            'consistency',
            'refresh',
            'timeout'
        ])
        return self.delete_by_id(document.doc_id, options)

    def delete_by_id(self, doc_id, options=None):
        """
        Deletes document by its id
        @param doc_id:
        @type doc_id: str
        @param options: query options
        @type options: dict
        @return:
        @rtype: pylastica.response.Response
        """
        if doc_id is None or doc_id == '':
            raise ValueError()
        doc_id = urllib.urlencode(doc_id)
        response = self.request(doc_id, pylastica.request.Request.DELETE, query=options)
        response_data = response.data
        if 'found' in response_data and not response_data['found']:
            raise pylastica.exception.NotFoundException("Document with id %s could not be found." % doc_id)
        return response

    def delete_by_query(self, query):
        """
        Delete documents based on the given query
        @param query:
        @type query: str or pylastica.query.Query
        @return:
        @rtype: pylastica.response.Response
        """
        query = pylastica.query.Query.create(query)
        return self.request('_query', pylastica.request.Request.DELETE, query.query)

    def delete(self):
        """
        Delete the current type from the index
        @return:
        @rtype: pylastica.response.Response
        """
        return self.request('', pylastica.request.Request.DELETE)

    def more_like_this(self, doc, params=None, query=None):
        """
        Perform a more like this query based on the given document
        @param doc:
        @type doc: pylastica.document.Document
        @param params: additional query params
        @type params: dict
        @param query: optional query to filter the more like this results
        @type query: str or dict or pylastica.query.Query
        @return:
        @rtype: pylastica.resultset.ResultSet
        """
        path = "%s/_mlt" % doc.doc_id
        query = pylastica.query.Query.create(query)
        response = self.request(path, pylastica.request.Request.GET, query.to_dict(), params)
        return pylastica.resultset.ResultSet(response, query)

    def request(self, path, method, data=None, query=None):
        """
        Make a call to the ES server based on this doc type
        @param path: path to call (url)
        @type path: str
        @param method: REST method
        @type method: str
        @param data: arguments as a dict
        @type data: dict
        @param query: query parameters
        @type query: dict
        @return:
        @rtype: pylastica.response.Response
        """
        path = '/'.join([self.name, path])
        return self.index.request(path, method, data, query)

    def set_serializer(self, serializer):
        """
        Set the serializer callable used in add_object
        @param serializer:
        @type serializer:
        @return:
        @rtype: self
        """
        self._serializer = serializer
        return self
