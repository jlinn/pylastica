__author__ = 'Joe Linn'

import pylastica

class Mapping(object):
    def __init__(self, doc_type=None, properties=None):
        """

        @param type: optional DocType object
        @type type: pylastica.doc_type.DocType
        @param properties:
        @type properties: dict
        """
        self._mapping = {}
        self._type = None
        if doc_type:
            self.doc_type = doc_type
        if properties:
            self.set_properties(properties)

    @property
    def doc_type(self):
        """
        Return the document type object
        @return:
        @rtype: pylastica.doc_type.DocType
        """
        return self._type

    @doc_type.setter
    def doc_type(self, doc_type):
        """

        @param doc_type:
        @type doc_type: pylastica.doc_type.DocType
        """
        assert isinstance(doc_type, pylastica.doc_type.DocType), "doc_type jmust be of type DocType: %r" % doc_type
        self._type = doc_type

    def set_properties(self, properties):
        """
        Set mapping properties
        @param properties:
        @type properties: dict
        @return:
        @rtype: self
        """
        return self.set_param('properties', properties)

    def set_meta(self, meta):
        """
        Set mapping meta
        @param meta:
        @type meta: dict
        @return:
        @rtype: self
        @see: http://www.elasticsearch.org/guide/reference/mapping/meta/
        """
        return self.set_param('_meta', meta)

    def set_source(self, source):
        """
        Sets source values
        @param source:
        @type source: dict
        @return:
        @rtype: self
        """
        return self.set_param('_source', source)

    def disable_source(self, enabled=False):
        """
        Disables the source in the index.
        @param enabled:
        @type enabled: bool
        @return:
        @rtype: self
        """
        return self.set_source({'enabled': enabled})

    def set_param(self, key, value):
        """
        Sets raw parameters.  See ES docs for options.
        @param key: key name
        @type key: str
        @param value:
        @type value: mixed
        @return:
        @rtype: self
        """
        self._mapping[key] = value
        return self

    def set_all_field(self, params):
        """
        Set params for the '_all' field
        @param params:
        @type params: dict
        @return:
        @rtype: self
        """
        return self.set_param('_all', params)

    def enable_all_field(self, enabled=True):
        """
        Enable (or disable) the '_all' field
        @param enabled: Enabled if True, disabled if False. Defaults to True.
        @type enabled: bool
        @return:
        @rtype: self
        """
        return self.set_all_field({'enabled': enabled})

    def set_ttl(self, params):
        """
        Set TTL
        @param params: ttl parameters
        @type params: dict
        @return:
        @rtype: self
        """
        return self.set_param('_ttl', params)

    def enable_ttl(self, enabled=True):
        """
        Enable TTL for all documents of this type
        @param enabled:
        @type enabled: bool
        @return:
        @rtype: self
        """
        return self.set_ttl({'enabled': enabled})

    def set_parent(self, doc_type):
        """
        Set parent doc type
        @param doc_type:
        @type doc_type: str
        @return:
        @rtype: self
        """
        return self.set_param('_parent', {'type': doc_type})

    def to_dict(self):
        """
        Convert the mapping to a dict
        @return:
        @rtype: dict
        """
        doc_type = self.doc_type
        if doc_type is None:
            raise pylastica.exception.InvalidException("doc_type must be set.")
        return {doc_type.name: self._mapping}

    def send(self):
        """
        Sends the mapping to the server
        @return:
        @rtype: pylastica.response.Response
        """
        return self.doc_type.request('_mapping', pylastica.request.Request.PUT, self.to_dict())

    @classmethod
    def create(cls, mapping):
        """
        Create a mapping object
        @param cls:
        @type cls:
        @param mapping: mapping object or properties dict
        @type mapping: pylastica.doc_type.Mapping or dict
        @return:
        @rtype: pylastica.doc_type.Mapping
        """
        if isinstance(mapping, dict):
            mapping_object = cls()
            mapping_object.set_properties(mapping)
        else:
            mapping_object = mapping
        assert isinstance(mapping_object, cls), "Invalid object type"
        return mapping_object
