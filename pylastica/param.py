__author__ = 'Joe Linn'

import json
import pylastica.exception
import pylastica.util


class Param(object):
    def __init__(self):
        self._params = {}
        self._rawParams = {}

    def to_dict(self):
        """
        Convert the params to a dict
        @return:
        @rtype: dict
        """
        data = {self._get_base_name(): self.params}
        if len(self._rawParams):
            data.update(self._rawParams)
        return data

    def _get_base_name(self):
        """
        Param's name
        @return:
        @rtype: str
        """
        return pylastica.util.get_param_name(self)

    def _set_raw_param(self, key, value):
        """
        Sets params not inside params dict
        @param key:
        @type key: str
        @param value:
        @type value: mixed
        @return:
        @rtype: self
        """
        self._rawParams[key] = value
        return self

    def set_param(self, key, value):
        """
        Set (overwrite) the value at the given key
        @param key: key to set
        @type key: str
        @param value: value
        @type value: mixed
        @return:
        @rtype: self
        """
        self._params[key] = value
        return self

    def add_param(self, key, value):
        """
        Add a param to the list at key
        @param key:
        @type key: str
        @param value:
        @type value: mixed
        @return:
        @rtype: self
        """
        if not key in self._params:
            self._params[key] = []
        self._params[key].append(value)
        return self

    def get_param(self, key):
        """
        Get a specific parameter
        @param key:
        @type key: str
        @return:
        @rtype: mixed
        """
        if not key in self._params:
            raise pylastica.exception.InvalidException("Param %s does not exist." % key)
        return self._params[key]

    def has_param(self, key):
        """
        Test if a param exists
        @param key:
        @type key: str
        @return:
        @rtype: bool
        """
        return key in self._params

    @property
    def params(self):
        """
        Get the params dict
        @return:
        @rtype: dict
        """
        return self._params

    @params.setter
    def params(self, params):
        """
        Set (overwrite) all params of this object
        @param params:
        @type params: dict
        """
        assert isinstance(params, dict), "params must be of type dict: %r" % params
        self._params = params

    def __str__(self):
        """
        @return:
        @rtype: str
        """
        return json.dumps(self.to_dict())

    def __unicode__(self):
        """

        @return:
        @rtype: unicode
        """
        return unicode(self.__str__())
