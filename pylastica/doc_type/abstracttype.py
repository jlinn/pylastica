__author__ = 'Joe Linn'

import abc
import pylastica

class AbstractType(pylastica.searchable.Searchable):
    __metaclass__ = abc.ABCMeta

    MAX_DOCS_PER_REQUEST = 1000

    _index_name = None  #name of index. Override this in implementing classes.
    _type_name = None   #name of document type. Override this in implementing classes.

    def __init__(self, client=None):
        """
        Reads index and type names from class properties _index_name and _type_name, which must be set in child classes.
        @param client: optional client object
        @type client: pylastica.client.Client
        """
        if client is None:
            client = pylastica.client.Client()
        if self._index_name is None:
            raise pylastica.exception.InvalidException("_index_name must be set!")
        if self._type_name is None:
            raise pylastica.exception.InvalidException("_type_name must be set!")
        self._client = client
        self._index = pylastica.index.Index(client, self._index_name)
        self._doc_type = pylastica.doc_type.DocType(self._index, self._type_name)
        self._mapping = {}
        self._index_params = {}
        self._source = True

    def create(self, recreate=False):
        """
        Creates the index and sets the mapping for this type
        @param recreate: if set to true, will recreate the index if it already exists
        @type recreate: bool
        """
        self.index.create(self._index_params, recreate)
        mapping = pylastica.doc_type.Mapping(self.doc_type)
        mapping.properties = self._mapping
        mapping.source = {'enabled': self._source}
        mapping.send()

    def create_search(self, query=None, options=None):
        """

        @param query:
        @type query: pylastica.query.Query
        @param options:
        @type options:  dict
        @return:
        @rtype: pylastica.search.Search
        """
        return self.doc_type.create_search(query, options)

    def count(self, query=None):
        """
        Counts results for a query. If no query is set, a MatchAll query is used.
        @param query: dict with all query data or a Query object
        @type query: dict or pylastica.query.Query
        @return: number of docs matching the query
        @rtype: int
        """
        return self.doc_type.count(query)

    @property
    def index(self):
        """
        Retrieve the index object
        @return:
        @rtype: pylastica.index.Index
        """
        return self._index

    @property
    def doc_type(self):
        """
        Return the document type object
        @return:
        @rtype: pylastica.doc_type.DocType
        """
        return self._doc_type

    def convert_date(self, date):
        """
        Converts given time to format: 1995-12-31T23:59:59Z
        This is the lucene date format
        @param date:
        @type date: int
        @return:
        @rtype: str
        """
        return pylastica.util.convert_date(date)
