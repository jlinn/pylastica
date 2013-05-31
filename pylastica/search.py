__author__ = 'Joe Linn'

#import pylastica
import pylastica.client
import pylastica.query

class Search(object):
    OPTION_SEARCH_TYPE = 'search_type'
    OPTION_ROUTING = 'routing'
    OPTION_PREFERENCE = 'preference'
    OPTION_VERSION = 'version'
    OPTION_TIMEOUT = 'timeout'
    OPTION_FROM = 'from'
    OPTION_SIZE = 'size'
    OPTION_SCROLL = 'scroll'
    OPTION_SCROLL_ID = 'scroll_id'

    SEARCH_TYPE_COUNT = 'count'
    SEARCH_TYPE_SCAN = 'scan'
    SEARCH_TYPE_DFS_QUERY_THEN_FETCH = 'dfs_query_then_fetch'
    SEARCH_TYPE_DFS_QUERY_AND_FETCH = 'dfs_query_and_fetch'
    SEARCH_TYPE_QUERY_THEN_FETCH = 'query_then_fetch'
    SEARCH_TYPE_QUERY_AND_FETCH = 'query_and_fetch'

    def __init__(self, client):
        """
        @param client:
        @type client: pylastica.client.Client
        """
        assert isinstance(client, pylastica.client.Client), "client must be an instance of Client: %r" % client
        self._client = client
        self._indices = []
        self._types = []
        self._query = None
        self._options = {}

    def add_index(self, index):
        """
        Add an index to the list
        @param index:
        @type index: str or pylastica.index.Index
        @return:
        @rtype: self
        """
        if isinstance(index, pylastica.index.Index):
            index = index.name
        assert isinstance(index, str), "Invalid param type: %r" % index
        self._indices.append(index)
        return self

    def add_indices(self, indices):
        """
        Add multiple indices to the internal list
        @param indices:
        @type indices: list of str or list of pylastica.index.Index
        @return:
        @rtype: self
        """
        for index in indices:
            self.add_index(index)
        return self

    def add_type(self, doc_type):
        """
        Add a type to the current search
        @param doc_type:
        @type doc_type: str or pylastica.doc_type.DocType
        @return:
        @rtype: self
        """
        if isinstance(doc_type, pylastica.doc_type.DocType):
            doc_type = doc_type.name
        assert isinstance(doc_type, str), "Invalid param type: %r" % doc_type
        self._types.append(doc_type)
        return self

    def add_types(self, doc_types):
        """
        Add multiple document types to the search
        @param doc_types:
        @type doc_types: list of str or list of pylastica.doc_type.DocType
        @return:
        @rtype: self
        """
        for doc_type in doc_types:
            self.add_type(doc_type)
        return self

    def set_query(self, query):
        """
        @param query:
        @type query: str or dict or pylastica.query.Query
        @return:
        @rtype: self
        """
        self._query = pylastica.query.Query.create(query)
        return self

    def set_option(self, key, value):
        """

        @param key:
        @type key: str
        @param value:
        @type value: mixed
        @return:
        @rtype: self
        """
        self._validate_option(key)
        self._options[key] = value
        return self

    def set_options(self, options):
        """
        Set all options. Clears existing options.
        @param options:
        @type options: dict
        @return:
        @rtype: self
        """
        self.clear_options()
        for key, value in options.iteritems():
            self.set_option(key, value)
        return self

    def clear_options(self):
        """

        @return:
        @rtype: self
        """
        self._options = {}
        return self

    def add_option(self, key, value):
        """
        Add an option
        @param key:
        @type key: str
        @param value:
        @type value: mixed
        @return:
        @rtype: self
        """
        self._validate_option(key)
        if key not in self._options:
            self._options[key] = []
        self._options[key].append(value)
        return self

    def has_option(self, key):
        """

        @param key:
        @type key: str
        @return:
        @rtype: bool
        """
        return key in self._options

    def get_option(self, key):
        """

        @param key:
        @type key: str
        @return:
        @rtype: mixed
        """
        if not self.has_option(key):
            raise pylastica.exception.InvalidException("Option %s does not exist." % key)
        return self._options[key]

    @property
    def options(self):
        """

        @return:
        @rtype: dict
        """
        return self._options

    @options.setter
    def options(self, options):
        """
        Set all options. Clears existing options.
        @param options:
        @type options: dict
        """
        self.set_options(options)

    @options.deleter
    def options(self):
        self.clear_options()

    def _validate_option(self, key):
        """

        @param key:
        @type key: key
        @return:
        @rtype: bool
        """
        valid_options = [
            self.OPTION_SEARCH_TYPE,
            self.OPTION_ROUTING,
            self.OPTION_PREFERENCE,
            self.OPTION_PREFERENCE,
            self.OPTION_VERSION,
            self.OPTION_TIMEOUT,
            self.OPTION_FROM,
            self.OPTION_SIZE,
            self.OPTION_SCROLL,
            self.OPTION_SCROLL_ID
        ]
        if key in valid_options:
            return True
        raise pylastica.exception.InvalidException("Invalid option: %s." % key)

    @property
    def client(self):
        """

        @return:
        @rtype: pylastica.client.Client
        """
        return self._client

    @property
    def indices(self):
        """

        @return:
        @rtype: list of str
        """
        return self._indices

    def has_indices(self):
        """

        @return:
        @rtype: bool
        """
        return len(self._indices) > 0

    def has_index(self, index):
        """

        @param index: index object or index name
        @type index: str or pylastica.index.Index
        @return:
        @rtype: bool
        """
        if isinstance(index, pylastica.index.Index):
            index = index.name
        return index in self._indices

    @property
    def doc_types(self):
        """
        Get a list of document types
        @return:
        @rtype: list of str
        """
        return self._types

    def has_doc_types(self):
        """

        @return:
        @rtype: bool
        """
        return len(self._types) > 0

    def has_doc_type(self, doc_type):
        """

        @param doc_type:
        @type doc_type: str or pylastica.doc_type.DocType
        @return:
        @rtype: bool
        """
        if isinstance(doc_type, pylastica.doc_type.DocType):
            doc_type = doc_type.name
        return doc_type in self._types

    @property
    def query(self):
        """

        @return:
        @rtype: pylastica.query.Query
        """
        if self._query is None:
            self._query = pylastica.query.Query.create('')
        return self._query

    @query.setter
    def query(self, query):
        """
        @param query:
        @type query: str or dict or pylastica.query.Query
        """
        self.set_query(query)

    @classmethod
    def create(cls, search_object):
        """
        Create a new search object
        @param cls:
        @type cls:
        @param search_object:
        @type search_object: pylastica.searchable.Searchable
        @return:
        @rtype: self
        """
        return search_object.create_search()

    @property
    def path(self):
        """
        Combines indices and types to get the search request path
        @return: search path (url)
        @rtype: str
        """
        indices = self.indices
        path = ''
        doc_types = self.doc_types
        if len(indices) == 0:
            if len(doc_types) != 0:
                path += '_all'
        else:
            path += ','.join(indices)
        if len(doc_types) != 0:
            path += '/' + ','.join(doc_types)
        return path + '/_search'

    def search(self, query=None, options=None):
        """
        Search in the set indices and types
        @param query:
        @type query: mixed
        @param options: optional limit or dict of options
        @type options: int or dict
        @return:
        @rtype: pylastica.resultset.ResultSet
        """
        self.set_options_and_query(options, query)
        query = self.query
        response = self.client.request(self.path, data=query.to_dict(), query=self.options)
        return pylastica.resultset.ResultSet(response, query)

    def count(self, query=None):
        """
        Counts results for a query. If no query is set, a MatchAll query is used.
        @param query: dict with all query data or a Query object
        @type query: dict or pylastica.query.Query
        @return: number of docs matching the query
        @rtype: int
        """
        self.set_options_and_query(None, query)
        query = self.query
        response = self.client.request(self.path, data=query.to_dict(), query={self.OPTION_SEARCH_TYPE: self.SEARCH_TYPE_COUNT})
        return pylastica.resultset.ResultSet(response, query).get_total_hits()

    def set_options_and_query(self, options=None, query=None):
        """

        @param options:
        @type options: int or dict
        @param query:
        @type query: str or dict or pylastica.query.Query
        @return:
        @rtype: self
        """
        if query is not None:
            self.query = query
        if isinstance(options, int):
            self._query.size = options
        elif isinstance(options, dict):
            if 'limit' in options:
                self._query.size = options['limit']
                del options['limit']
            if 'explain' in options:
                self._query.explain = options['explain']
                del options['explain']
            self.set_options(options)
        return self
