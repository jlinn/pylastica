__author__ = 'Joe Linn'

import pylastica

class Stats(object):

    def __init__(self, index):
        """
        @param index:
        @type index: pylastica.index.Index
        """
        assert isinstance(index, pylastica.index.Index), "index must be of type Index: %r" % index
        self._index = index
        self._response = None
        self._data = {}
        self.refresh()

    @property
    def data(self):
        """
        Returns the raw stats info
        @return:
        @rtype: dict
        """
        return self._data

    def get(self, *args):
        """
        Returns data based on keys in args
        @param args: keys of data to return
        @type args: str
        @return:
        @rtype: dict or None
        """
        #TODO: this behavior doesn't seem right. If multiple args can be passed, why only return data for the first one?
        data = self.data
        for arg in args:
            if arg in data:
                data = data[arg]
            else:
                return None
        return data

    @property
    def index(self):
        """
        Return the index object
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
        Reloads the status data for this object
        """
        self._response = self.index.request('_stats', pylastica.request.Request.GET)
        self._data = self.response.data
