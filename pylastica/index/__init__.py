__author__ = 'Joe Linn'

import pylastica.searchable
from .settings import *
from .stats import *
from .status import *


class Index(pylastica.searchable.Searchable):
    def __init__(self, client, name):
        """

        @param client:
        @type client: pylastica.client.Client
        @param name: index name
        @type name: str
        """
        assert isinstance(client, pylastica.client.Client), "client must be an instance of Client: %r" % client
        name = str(name)
        assert isinstance(name, str), "name must be a str: %r" % name
        self._name = name
        self._client = client

    def get_doc_type(self, doc_type):
        """
        Return a DocType object for the current index with the given type name
        @param doc_type: type name
        @type doc_type: str
        @return:
        @rtype: pylastica.doc_type.DocType
        """
        return pylastica.doc_type.DocType(self, doc_type)

    @property
    def status(self):
        """

        @return:
        @rtype: pylastica.index.Status
        """
        return self.get_status()

    def get_status(self):
        """
        Returns the current status of the idnex
        @return:
        @rtype: pylastica.index.Status
        """
        return pylastica.index.Status(self)

    @property
    def stats(self):
        """

        @return:
        @rtype: pylastica.index.Stats
        """
        return self.get_stats()

    def get_stats(self):
        """
        Return index stats
        @return:
        @rtype: pylastica.index.Stats
        """
        return pylastica.index.Stats(self)

    @property
    def mapping(self):
        """
        Get all the type mappings for an index
        @return:
        @rtype: dict
        """
        return self.request('_mapping', pylastica.request.Request.GET).data

    @property
    def settings(self):
        """
        Return the index settings object
        @return:
        @rtype: pylastica.index.Settings
        """
        return pylastica.index.Settings(self)

    def add_documents(self, docs):
        """
        Use _bulk to send docs to the server
        @param docs:
        @type docs: list of pylastica.document.Document
        @return:
        @rtype: pylastica.bulk.ResponseSet
        """
        for doc in docs:
            doc.index = self.name
        return self.client.add_documents(docs)

    def delete(self):
        """
        Delete this index
        @return:
        @rtype: pylastica.response.Response
        """
        return self.request('', pylastica.request.Request.DELETE)

    def optimize(self, args=None):
        """
        Optimizes a search index
        @see: http://www.elasticsearch.org/guide/reference/api/admin-indices-optimize.html
        @param args: optional
        @type args: dict
        @return:
        @rtype: dict
        """
        return self.request('_optimize', pylastica.request.Request.POST, args)

    def refresh(self):
        """
        Refresh the index
        @return:
        @rtype: pylastica.response.Response
        """
        return self.request('_refresh', pylastica.request.Request.POST)

    def create(self, args=None, options=None):
        """
        Creates a new index with the given args
        @see: http://www.elasticsearch.org/guide/reference/api/admin-indices-create-index.html
        @param args: optional
        @type args: dict
        @param options: bool: deletes index first if it exists (defaults to False); dict: dictionary of options
        @type options: bool or dict
        @return: server response
        @rtype: pylastica.response.Response
        """
        path = ''
        query = {}
        if isinstance(options, bool):
            if options:
                try:
                    self.delete()
                except pylastica.exception.ResponseException:
                    #index doesn't exist yet
                    pass
        else:
            if isinstance(options, dict):
                for key, value in options.iteritems():
                    if key == 'recreate':
                        try:
                            self.delete()
                        except pylastica.exception.ResponseException:
                            #index doesn't exist yet
                            pass
                    elif key == 'routing':
                        query = {'routing': value}
                    else:
                        raise pylastica.exception.InvalidException("Invalid option: %s" % key)
        return self.request(path, pylastica.request.Request.PUT, args, query)

    def exists(self):
        """
        Checks if the given index exists
        @return:
        @rtype: bool
        """
        response = self._client.request('_cluster/state', pylastica.request.Request.GET, query={'filter_indices': self.name})
        return self.name in response.data['metadata']['indices']

    def create_search(self, query=None, options=None):
        """

        @param query:
        @type query: pylastica.query.Query
        @param options:
        @type options:  dict
        @return:
        @rtype: pylastica.search.Search
        """
        search = pylastica.search.Search(self.client)
        search.add_index(self)
        search.set_options_and_query(options, query)
        return search

    def search(self, query=None, options=None):
        """
        Searches this index
        @param query: dict of query data or Query object
        @type query: string or dict or pylastica.query.Query or pylastica.query.AbstractQuery or pylastica.suggest.Suggest
        @param options: optional dict of options or integer result limit
        @type options: dict or int
        @return:
        @rtype: pylastica.resultset.ResultSet
        """
        return self.create_search(query, options).search()

    def count(self, query=None):
        """
        Counts results for a query. If no query is set, a MatchAll query is used.
        @param query: dict with all query data or a Query object
        @type query: dict or pylastica.query.Query
        @return: number of docs matching the query
        @rtype: int
        """
        return self.create_search(query).count()

    def open(self):
        """
        Open the index
        @return:
        @rtype: pylastica.response.Response
        """
        return self.request('_open', pylastica.request.Request.POST)

    def close(self):
        """
        Close the index
        @return:
        @rtype: pylastica.response.Response
        """
        return self.request('_close', pylastica.request.Request.POST)

    @property
    def name(self):
        """
        Returns the name of the index
        @return:
        @rtype: str
        """
        return self._name

    @property
    def client(self):
        """
        Returns the client object
        @return:
        @rtype: pylastica.client.Client
        """
        return self._client

    def add_alias(self, name, replace=False):
        """
        Adds an alias to the current index
        @param name: alias name
        @type name: str
        @param replace: if True, existing alias of the same name will be replaced
        @type replace: bool
        @return:
        @rtype: pylastica.response.Response
        """
        data = {'actions': []}
        if replace:
            status = pylastica.Status(self.client)
            for index in status.get_indices_with_alias(name):
                data['actions'].append({
                    'remove':{
                        'index': index.name,
                        'alias': name
                    }
                })
        data['actions'].append({
            'add':{
                'index': self.name,
                'alias': name
            }
        })
        return self.client.request('_aliases', pylastica.request.Request.POST, data)

    def remove_alias(self, name):
        """
        Removes an alias of the given name pointing to the current index
        @param name:
        @type name: str
        @return:
        @rtype: pylastica.response.Response
        """
        return self.request('_alias/%s' % name, pylastica.request.Request.DELETE)

    def clear_cache(self):
        """
        Clears the cache of this index
        @return:
        @rtype: pylastica.response.Response
        """
        return self.request('_cache/clear', pylastica.request.Request.POST)

    def flush(self):
        """
        Flushes the index to storage
        @return:
        @rtype: pylastica.response.Response
        """
        return self.request('_flush', pylastica.request.Request.POST)

    def set_settings(self, data):
        """
        Can be used to change settings during runtime.
        @param data:
        @type data: dict
        @return:
        @rtype: pylastica.response.Response
        """
        return self.request('_settings', pylastica.request.Request.PUT, data)

    def request(self, path, method, data=None, query=None):
        """
        Make a call to the ES server based on the current index
        @param path: url
        @type path: str
        @param method: REST method
        @type method: str
        @param data: optional request data
        @type data: dict
        @param query: optional query parameters
        @type query: dict
        @return:
        @rtype: pylastica.response.Response
        """
        path = '/'.join([self.name, path])
        return self.client.request(path, method, data, query)
