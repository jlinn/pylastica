__author__ = 'Joe Linn'

import pylastica.index

class Status(object):
    def __init__(self, client):
        """

        @param client:
        @type client: pylastica.client.Client
        """
        super(Status, self).__init__()
        self._client = client
        self._data = None
        self._response = None
        self.refresh()

    @property
    def data(self):
        """
        Get status data
        @return:
        @rtype: dict
        """
        return self._data

    @property
    def index_statuses(self):
        """
        Get status objects of all indices
        @return:
        @rtype: list of pylastica.index.status.Status
        """
        return [pylastica.index.Status(pylastica.index.Index(self._client, name))for name in self.index_names]

    @property
    def index_names(self):
        """
        Get the names of existing indices
        @return:
        @rtype: list of str
        """
        return [name for name in self._data['indices']] if len(self._data['indices']) else []

    def index_exists(self, name):
        """
        Check if the given index exists
        @param name: index name
        @type name: str
        @return:
        @rtype: bool
        """
        return name in self.index_names

    def alias_exists(self, alias):
        """
        Determine if the given alias exists
        @param alias:
        @type alias: str
        @return:
        @rtype: bool
        """
        response = self._client.request('/_alias/%s' % alias)
        if response.has_error() and ('AliasMissingException' in response.error or response.status == '404'):
            return False
        return True

    def get_indices_with_alias(self, alias):
        """
        Get a list of all indices which share the given alias
        @param alias:
        @type alias: str
        @return:
        @rtype: list of pylastica.index.Index
        @raise: pylastica.exception.AliasMissingException if the requested alias does not exist
        """
        response = self._client.request('_alias/%s' % alias)
        if response.has_error() and ('AliasMissingException' in response.error or response.status == '404'):
            #the requested alias does not exist
            return []
        indices = response.data
        return [pylastica.index.Index(self._client, name) for name in indices]

    @property
    def response(self):
        """
        Return the response object
        @return:
        @rtype: pylastica.response.Response
        """
        return self._response

    @property
    def shards(self):
        """
        Return shards info
        @return:
        @rtype: dict
        """
        return self._data['shards']

    def refresh(self):
        """
        Refresh the status object
        @return:
        @rtype: void
        """
        self._response = self._client.request('_status')
        self._data = self.response.data

    @property
    def server_status(self):
        """
        Get server status
        @return:
        @rtype: dict
        """
        return self._client.request('').data
