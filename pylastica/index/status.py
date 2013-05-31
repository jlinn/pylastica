__author__ = 'Joe Linn'

import pylastica

class Status(object):
    def __init__(self, index):
        """
        @param index:
        @type index: pylastica.index.Index
        """
        assert isinstance(index, pylastica.index.Index), "index must be an instance of Index: %r" % index
        self._index = index
        self._response = None
        self._data = {}
        self.refresh()

    @property
    def data(self):
        """
        Returns all status info
        @return:
        @rtype: dict
        """
        return self._data

    def get(self, *args):
        """
        Returns the entry in the internal data based on the params.
        @param args:
        @type args: str
        @return:
        @rtype: dict or None
        """
        data = self.data
        data = data['indices'][self.index.name]
        for arg in args:
            if arg in data:
                data = data[arg]
            else:
                return None
        return data

    @property
    def aliases(self):
        """
        Returns all index aliases
        @return:
        @rtype: list
        """
        data = self.index.request('_aliases', pylastica.request.Request.GET).data[self.index.name]
        if 'aliases' not in data:
            raise pylastica.exception.NotFoundException("Alias data for index %s not found." % self.index.name)
        return [name for name in data['aliases']]

    def has_alias(self, alias):
        """
        Checks if the index has the given alias
        @param alias: alias name
        @type alias: str
        @return:
        @rtype: bool
        """
        return alias in self.aliases

    @property
    def settings(self):
        """
        @return: Index settings
        @rtype: dict
        """
        response_data = self.index.request('_settings', pylastica.request.Request.GET).data
        return response_data[self.index.name]['settings']

    @property
    def index(self):
        """
        get the index object
        @return:
        @rtype: pylastica.index.Index
        """
        return self._index

    @property
    def response(self):
        """
        Return the response object
        @return:
        @rtype: pylastica.response.Response
        """
        return self._response

    def refresh(self):
        """
        Reloads all status data for this object
        """
        self._response = self.index.request('_status', pylastica.request.Request.GET)
        self._data = self.response.data
