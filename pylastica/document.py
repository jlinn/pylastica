__author__ = 'Joe Linn'

import base64
import pylastica.param
from pylastica.bulk.action import Action


class Document(pylastica.param.Param):
    OP_TYPE_CREATE = Action.OP_TYPE_CREATE

    def __init__(self, doc_id=None, data=None, doc_type=None, index=None):
        """

        @param doc_id:
        @type doc_id:
        @param data:
        @type data:
        @param doc_type:
        @type doc_type:
        @param index:
        @type index:
        @return:
        @rtype:
        """
        super(Document, self).__init__()
        self._data = {}
        self._script = None
        self._auto_populate = False
        self._doc_as_upsert = False
        self._upsert = None
        self.doc_id = doc_id
        if data is not None:
            self.data = data
        self.doc_type = doc_type
        self.index = index

    @property
    def doc_id(self):
        """
        Get the document id
        @return:
        @rtype: str
        """
        return self.get_param('_id') if self.has_param('_id') else ''

    @doc_id.setter
    def doc_id(self, doc_id):
        """
        Set the document id
        @param doc_id:
        @type doc_id: str
        """
        if doc_id is not None:
            self.set_param('_id', str(doc_id))

    def has_id(self):
        """

        @return:
        @rtype: bool
        """
        return self.has_param('_id') and len(self.doc_id) > 0

    def get(self, key):
        """
        Retrieve a piece of data from this document
        @param key:
        @type key: str
        @return:
        @rtype: mixed
        """
        if not self.has(key):
            raise pylastica.exception.InvalidException("Field %s does not exist." % key)
        return self._data[key]

    def set(self, key, value):
        """
        Set a field
        @param key:
        @type key:  str
        @param value:
        @type value: mixed
        @return:
        @rtype: self
        """
        assert isinstance(self._data, dict), "Document data is serialized data. Data creation is forbidden."
        self._data[key] = value
        return self

    def has(self, key):
        """
        Determine if a field exists in this document
        @param key:
        @type key: str
        @return:
        @rtype: bool
        """
        return isinstance(self._data, dict) and key in self._data

    def remove(self, key):
        """
        Remove a field from the document
        @param key:
        @type key: str
        @return:
        @rtype: self
        """
        if not self.has(key):
            raise pylastica.exception.InvalidException("Field %s does not exist." % key)
        del self._data[key]
        return self

    def add(self, key, value):
        """
        Add the given key / value pair to the document
        @param key:
        @type key: str
        @param value:
        @type value: mixed
        @return:
        @rtype: self
        """
        return self.set(key, value)

    def add_file(self, key, file_path, mime_type=None):
        """
        Adds a file to the index. The attachments plugin must be installed before using this feature.
        ./bin/plugin -install elasticsearch/elasticsearch-mapper-attachments/1.6.0
        @see http://tika.apache.org/0.7/formats.html
        @param key: key of file
        @type key: str
        @param file_path: path of the file
        @type file_path: str
        @param mime_type: optional header MIME type
        @type mime_type: str
        @return:
        @rtype: self
        """
        value = base64.b64encode(open(file_path, 'rb').read())
        if mime_type is not None:
            value = {
                '_content_type': mime_type,
                '_name': file_path,
                'content': value
            }
        return self.set(key, value)

    def add_file_content(self, key, content):
        """
        Add file content to the document
        @param key:
        @type key: str
        @param content: raw file content
        @type content: str
        @return:
        @rtype: self
        """
        return self.set(key, base64.b64encode(content))

    def add_geopoint(self, key, lat, lon):
        """
        Add a geopoint to the document
        @param key:
        @type key: str
        @param lat: latitude
        @type lat: float
        @param lon: longitude
        @type lon: float
        @return:
        @rtype: self
        """
        return self.set(key, {
            'lat': lat,
            'lon': lon
        })

    @property
    def data(self):
        """

        @return:
        @rtype: dict
        """
        return self._data

    @data.setter
    def data(self, data):
        """
        Overwrites the current document data with the given data
        @param data:
        @type data: dict or str
        """
        self._data = data

    def set_data(self, data):
        """
        Overwrites the current document data with the given data
        @param data:
        @type data: dict or str
        @return:
        @rtype: self
        """
        self._data = data
        return self

    @property
    def ttl(self):
        """
        Get the document's ttl
        @return:
        @rtype: str or int
        """
        return self.get_param('_ttl')

    @ttl.setter
    def ttl(self, ttl):
        """
        Set the ttl
        @param ttl:
        @type ttl: str or int
        """
        self.set_param('_ttl', ttl)

    def has_ttl(self):
        """

        @return:
        @rtype: bool
        """
        return self.has_param('_ttl')

    @property
    def doc_type(self):
        """
        Return document type
        @return:
        @rtype: str
        """
        return self.get_param('_type')

    @doc_type.setter
    def doc_type(self, doc_type):
        """
        Set document type
        @param doc_type:
        @type doc_type: str or pylastica.doc_type.DocType
        """
        if isinstance(doc_type, pylastica.doc_type.DocType):
            self.index = doc_type.index
            doc_type = doc_type.name
        self.set_param('_type', doc_type)

    @property
    def index(self):
        """
        Return the document's index name
        @return:
        @rtype: str
        """
        return self.get_param('_index')

    @index.setter
    def index(self, index):
        """
        Set the document's index name
        @param index:
        @type index: str or pylastica.index.Index
        """
        if isinstance(index, pylastica.index.Index):
            index = index.name
        self.set_param('_index', index)

    @property
    def version(self):
        """
        Get the document's version
        @return:
        @rtype: int
        """
        return self.get_param('_version')

    @version.setter
    def version(self, version):
        """
        Set the version of the document for use with optimistic concurrency control
        @param version:
        @type version:  int
        """
        self.set_param('_version', int(version))

    def has_version(self):
        """
        Determine whether or not the document has a version
        @return:
        @rtype: bool
        """
        return self.has_param('_version')

    @property
    def version_type(self):
        """
        Returns the document's version type
        @return:
        @rtype: str or int
        """
        return self.get_param('_version_type')

    @version_type.setter
    def version_type(self, version_type):
        """
        Set the document's version type
        @see: http://www.elasticsearch.org/guide/reference/api/index_.html
        @param version_type:
        @type version_type: int
        """
        self.set_param('_version_type', version_type)

    def has_version_type(self):
        """

        @return:
        @rtype: bool
        """
        return self.has_param('_version_type')

    @property
    def parent(self):
        """
        Returns the parent document's id
        @return:
        @rtype: str
        """
        return self.get_param('_parent')

    @parent.setter
    def parent(self, parent):
        """
        Set the parent document's id
        @param parent:
        @type parent: str or int
        """
        self.set_param('_parent', parent)

    def has_parent(self):
        """

        @return:
        @rtype: bool
        """
        return self.has_param('_parent')

    @property
    def op_type(self):
        """
        Return the operation type
        @return:
        @rtype: str
        """
        return self.get_param('_op_type')

    @op_type.setter
    def op_type(self, op_type):
        """
        Set the operation type
        @param op_type:
        @type op_type: str
        """
        self.set_param('_op_type', op_type)

    def has_op_type(self):
        """

        @return:
        @rtype: bool
        """
        return self.has_param('_op_type')

    @property
    def percolate(self):
        """
        Return percolate parameter
        @return:
        @rtype: str
        """
        return self.get_param('_percolate')

    @percolate.setter
    def percolate(self, percolate='*'):
        """
        Set percolate parameter
        @param percolate:
        @type percolate: str
        """
        self.set_param('_percolate', percolate)

    def has_percolate(self):
        """

        @return:
        @rtype: bool
        """
        return self.has_param('_percolate')

    @property
    def routing(self):
        """
        Return the routing for this document
        @return:
        @rtype: str
        """
        return self.get_param('_routing')

    @routing.setter
    def routing(self, routing):
        """
        Set routing for this document
        @param routing:
        @type routing: str
        """
        self.set_param('_routing', routing)

    def has_routing(self):
        """

        @return:
        @rtype: bool
        """
        return self.has_param('_routing')

    @property
    def fields(self):
        """

        @return:
        @rtype: str
        """
        return self.get_param('_fields')

    @fields.setter
    def fields(self, fields):
        """
        Set document fields
        @param fields:
        @type fields: str or list of str
        """
        if isinstance(fields, list):
            fields = ','.join(fields)
        self.set_param('_fields', fields)

    def has_fields(self):
        """

        @return:
        @rtype: bool
        """
        return self.has_param('_fields')

    def set_fields_source(self):
        """

        @return:
        @rtype: self
        """
        self.fields = '_source'
        return self

    @property
    def retry_on_conflict(self):
        """

        @return:
        @rtype: int
        """
        return self.get_param('_retry_on_conflict')

    @retry_on_conflict.setter
    def retry_on_conflict(self, retry):
        """

        @param retry:
        @type retry: int
        """
        self.set_param('_retry_on_conflict', int(retry))

    def has_retry_on_conflict(self):
        """

        @return:
        @rtype: bool
        """
        return self.has_param('_retry_on_conflict')

    @property
    def timestamp(self):
        """
        Return the document's timestamp
        @return:
        @rtype: int
        """
        return self.get_param('_timestamp')

    @timestamp.setter
    def timestamp(self, timestamp):
        """
        Set the document's timestamp
        @param timestamp:
        @type timestamp: int
        """
        self.set_param('_timestamp', timestamp)

    def has_timestamp(self):
        """

        @return:
        @rtype: bool
        """
        return self.has_param('_timestamp')

    @property
    def refresh(self):
        """

        @return:
        @rtype: bool
        """
        return self.get_param('_refresh')

    @refresh.setter
    def refresh(self, refresh=True):
        """

        @param refresh:
        @type refresh: bool
        """
        self.set_param('_refresh', bool(refresh))

    def has_refresh(self):
        """

        @return:
        @rtype: bool
        """
        return self.has_param('_refresh')

    @property
    def timeout(self):
        """

        @return:
        @rtype: str
        """
        return self.get_param('_timeout')

    @timeout.setter
    def timeout(self, timeout):
        """

        @param timeout:
        @type timeout: str
        """
        self.set_param('_timeout', timeout)

    def has_timeout(self):
        """

        @return:
        @rtype: bool
        """
        return self.has_param('_timeout')

    @property
    def consistency(self):
        """

        @return:
        @rtype: str
        """
        return self.get_param('_consistency')

    @consistency.setter
    def consistency(self, consistency):
        """

        @param consistency:
        @type consistency: str
        """
        self.set_param('_consistency', consistency)

    def has_consistency(self):
        """

        @return:
        @rtype: bool
        """
        return self.has_param('_consistency')

    @property
    def replication(self):
        """

        @return:
        @rtype: str
        """
        return self.get_param('_replication')

    @replication.setter
    def replication(self, replication):
        """

        @param replication:
        @type replication: str
        """
        self.set_param('_replication', replication)

    def has_replication(self):
        """

        @return:
        @rtype: bool
        """
        return self.has_param('_replication')

    @property
    def script(self):
        """

        @return:
        @rtype: pylastica.script.Script
        """
        raise pylastica.exception.NotImplementedException("The script getter is no longer available.")

    @script.setter
    def script(self, script):
        """

        @param script:
        @type script: pylastica.script.Script or dict or str
        """
        raise pylastica.exception.NotImplementedException("The script setter is no longer available.")

    @property
    def upsert(self):
        """

        @return:
        @rtype: dict
        """
        return self._upsert

    @upsert.setter
    def upsert(self, upsert):
        """

        @param upsert:
        @type upsert: dict
        """
        document = Document.create(upsert)
        self._upsert = document

    def has_upsert(self):
        """

        @return:
        @rtype: bool
        """
        return self._upsert is not None

    def has_script(self):
        """

        @return:
        @rtype: bool
        """
        raise pylastica.exception.NotImplementedException("has_script() is no longer available.")

    @property
    def doc_as_upsert(self):
        """

        @return:
        @rtype: bool
        """
        return self._doc_as_upsert

    @doc_as_upsert.setter
    def doc_as_upsert(self, value):
        """

        @param value:
        @type value: bool
        """
        self._doc_as_upsert = bool(value)

    @property
    def auto_populate(self):
        """

        @return:
        @rtype: bool
        """
        return self._auto_populate

    @auto_populate.setter
    def auto_populate(self, auto_populate):
        """

        @param auto_populate:
        @type auto_populate: bool
        """
        self._auto_populate = bool(auto_populate)

    def to_dict(self):
        """
        Return the document as a dict
        @return:
        @rtype: dict
        """
        doc = self.params
        doc['_source'] = self.data
        return doc

    def get_options(self, fields=None, with_underscore=False):
        """

        @param fields: if None, all options will be returned
        @type fields: list of str
        @param with_underscore: determines whether or not option keys should contaion underscore prefix
        @type with_underscore: bool
        @return:
        @rtype: dict
        """
        if fields is not None:
            data = {}
            for field in fields:
                key = '_' + field.lstrip('_')
                if self.has_param(key) and str(self.get_param(key)) != '':
                    data[key] = self.get_param(key)
        else:
            data = self.params
        if not with_underscore:
            data = {key.lstrip('_'): value for key, value in data.iteritems()}
        return data

    @classmethod
    def create(cls, data):
        """

        @param cls:
        @type cls:
        @param data:
        @type data: dict or Document
        @return:
        @rtype: Document
        """
        if isinstance(data, cls):
            return data
        elif isinstance(data, dict):
            return cls('', data)
        else:
            raise pylastica.exception.InvalidException("Failed to create document. Invalid data provided: %r" % data)