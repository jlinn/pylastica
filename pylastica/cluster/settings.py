__author__ = 'Joe Linn'

import pylastica.client

class Settings(object):
    def __init__(self, client):
        """
        @param client:
        @type client: pylastica.client.Client
        """
        super(Settings, self).__init__()
        assert isinstance(client, pylastica.client.Client), "client must be an instance of pylastica.client.Client: %r" % client
        self._client = client

    def get(self):
        """
        Returns settings data
        @return: settings data (persistent and transient)
        @rtype: dict
        """
        return self.request().data

    def get_persistent(self, setting=''):
        """
        Returns the current persistent settings of the cluster
        @param setting: Optional. If set, only the specified setting is returned
        @type setting: str
        @return:
        @rtype: dict or str or None
        """
        settings = self.get()['persistent']
        if setting != '':
            if setting in settings:
                return settings[setting]
            else:
                return None
        return settings

    def get_transient(self, setting=''):
        """
        Returns the current transient settings of the cluster
        @param setting: Optional. If set, only returns the specified setting.
        @type setting: str
        @return:
        @rtype: dict or string or None
        """
        settings = self.get()['transient']
        if setting != '':
            if setting in settings:
                return settings[setting]
            else:
                return None
        return settings

    def set_persistent(self, key, value):
        """
        Set a persistent setting
        @param key:
        @type key: str
        @param value:
        @type value: str
        @return:
        @rtype: pylastica.response.Response
        """
        return self.set({'persistent': {key: value}})

    def set_transient(self, key, value):
        """
        Set a transient setting
        @param key:
        @type key: str
        @param value:
        @type value: str
        @return:
        @rtype: pylastica.response.Response
        """
        return self.set({'transient': {key: value}})

    def set_read_only(self, read_only=True, persistent=False):
        """
        Set the cluster to read-only
        @param read_only:
        @type read_only: bool
        @param persistent: If true, the setting is persistent
        @type persistent: bool
        @return:
        @rtype: pylastica.response.Response
        """
        key = 'cluster.blocks.read_only'
        if persistent:
            return self.set_persistent(key, read_only)
        else:
            return self.set_transient(key, read_only)

    def set(self, settings):
        """
        Set settings for the cluster
        @param settings: raw settings (including persistent or transient)
        @type settings: dict
        @return:
        @rtype: pylastica.response.Response
        """
        return self.request(settings, pylastica.request.Request.PUT)

    @property
    def client(self):
        """
        Get the client object
        @return:
        @rtype: pylastica.client.Client
        """
        return self._client

    def request(self, data=None, method=pylastica.request.Request.GET):
        """
        Sends a settings request
        @param data: optional data dict
        @type data: dict
        @param method: optional HTTP method
        @type method: str
        @return:
        @rtype: pylastica.response.Response
        """
        return self.client.request('_cluster/settings', method, data)
