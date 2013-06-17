__author__ = 'Joe Linn'

import abc
import pylastica.param


class AbstractFacet(pylastica.param.Param):
    __metaclass__ = abc.ABCMeta

    def __init__(self, name):
        """
        @param name: the name of the facet
        @type name: str
        """
        super(AbstractFacet, self).__init__()
        self._facet = {}
        self.name = name

    @property
    def name(self):
        """
        Get the name of this facet
        @return:
        @rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Set the name of this facet.
        @param name:
        @type name: str
        """
        assert isinstance(name, str) and name != '', "name must be a string: %r" % name
        self._name = name

    def set_filter(self, facet_filter):
        """
        Set a filter for this facet
        @param facet_filter: a filter to apply on the facet
        @type facet_filter: pylastica.filter.AbstractFilter
        @return:
        @rtype: self
        """
        if not isinstance(facet_filter, pylastica.filter.AbstractFilter):
            raise TypeError("facet_filter must be an instance of an implementation of AbstractFilter: %r" % facet_filter)
        return self._set_facet_param('facet_filter', facet_filter.to_dict())

    def set_global(self, glob=True):
        """
        Sets the flag to either run the facet globally or bound to the current search query
        @param glob:
        @type glob: bool
        @return:
        @rtype: self
        """
        return self._set_facet_param('global', bool(glob))

    def set_nested(self, nested_path):
        """
        Set the path for nexted documents
        @param nested_path: document path
        @type nested_path: str
        @return:
        @rtype: self
        """
        return self._set_facet_param('nested', nested_path)

    def set_scope(self, scope):
        """
        Set the scope
        @param scope:
        @type scope: str
        @return:
        @rtype: self
        """
        return self._set_facet_param('scope', scope)

    def to_dict(self):
        """

        @return:
        @rtype: dict
        """
        return self._facet

    def _set_facet_param(self, key, value):
        """
        Sets a param for the facet. Each facet implementation must handle its own parameters.
        @param key:
        @type key: str
        @param value:
        @type value: mixed
        @return:
        @rtype: self
        """
        self._facet[key] = value
        return self
