__author__ = 'Joe Linn'

#import pylastica
import pylastica.request

class Settings(object):
    DEFAULT_REFRESH_INTERVAL = '1s'

    def __init__(self, index):
        """

        @param index:
        @type index: pylastica.index.Index
        """
        assert isinstance(index, pylastica.index.Index), "index must be of type Index: %r" % index
        self._index = index
        self._response = None
        self._data = {}

    def get(self, setting=None):
        """
        Returns the current settings of the index
        @param setting: optional setting name to return
        @type setting: str
        @return:
        @rtype: dict or str or None
        """
        data = self.request().data
        settings = data[self.index.name]['settings']
        if setting is not None:
            if "index.%s" % setting in settings:
                return settings["index.%s" % setting]
            else:
                return None
        return settings

    def set(self, data):
        """
        Set or update index settings
        @param data: arguments
        @type data: dict
        @return:
        @rtype: pylastica.response.Response
        """
        return self.request(data, pylastica.request.Request.PUT)

    def set_number_of_replicas(self, replicas):
        """
        Set the number of replicas
        @param replicas:
        @type replicas: int
        @return:
        @rtype: pylastica.response.Response
        """
        return self.set({'number_of_replicas': int(replicas)})

    def set_read_only(self, read_only=True):
        """
        Sets the index to read only
        @param read_only:
        @type read_only: bool
        @return:
        @rtype: pylastica.response.Response
        """
        return self.set({'blocks.read_only': read_only})

    def get_blocks_read(self):
        """

        @return:
        @rtype: bool
        """
        return bool(self.get('blocks.read'))

    def set_blocks_read(self, state=True):
        """

        @param state:
        @type state: bool
        @return:
        @rtype: pylastica.response.Response
        """
        state = 1 if state else 0
        return self.set({'blocks.read': state})

    def get_blocks_write(self):
        """

        @return:
        @rtype: bool
        """
        return self.get('blocks.write')

    def set_blocks_write(self, state=True):
        """

        @param state:
        @type state: bool
        @return:
        @rtype: pylastica.response.Response
        """
        state = 1 if state else 0
        return self.set({'blocks.write': int(state)})

    def get_blocks_metadata(self):
        """

        @return:
        @rtype: bool
        """
        return bool(self.get('blocks.metadata'))

    def set_blocks_metadata(self, state=True):
        """

        @param state:
        @type state: bool
        @return:
        @rtype: pylastica.response.Response
        """
        state = 1 if state else 0
        return self.set({'blocks.metadata': int(state)})

    def set_refresh_interval(self, interval):
        """
        Set the index refresh interval
        @param interval: 3s for 3 seconds, 5m for 5 minutes, etc. -1 to disable
        @type interval: str
        @return:
        @rtype: pylastica.response.Response
        """
        return self.set({'refresh_interval': interval})

    def get_refresh_interval(self):
        """
        Get the refresh interval
        @return:
        @rtype: str
        """
        interval = self.get('refresh_interval')
        if interval is None or interval == '':
            interval = self.DEFAULT_REFRESH_INTERVAL
        return interval

    def get_merge_policy_type(self):
        """
        Return merge policy
        @return:
        @rtype: str
        """
        return self.get('merge.policy.type')

    def set_merge_policy_type(self, type):
        """
        Set merge policy

        @param type:
        @type type: str
        @return:
        @rtype: pylastica.response.Response
        """
        self.index.close()
        response = self.set({'merge.policy.type': type})
        self.index.open()
        return response

    def set_merge_policy(self, key, value):
        """
        Set specific merge policies
        @param key: merge policy key (expunge_deletes_allowed, for example)
        @type key: str
        @param value:
        @type value: str
        @return:
        @rtype: pylastica.response.Response
        """
        self.index.close()
        response = self.set({'merge.policy.%s' % key: value})
        self.index.open()
        return response

    def get_merge_policy(self, key):
        """
        Returns a specific merge policy value
        @param key: merge policy key
        @type key: str
        @return:
        @rtype: str
        """
        return self.get('merge.policy.%s' % key)

    @property
    def index(self):
        """
        Return the index object
        @return:
        @rtype: pylastica.index.Index
        """
        return self._index

    def request(self, data=None, method=pylastica.request.Request.GET):
        """
        Update the given settings for the index
        @param data: optional data dictionary
        @type data: dict
        @param method: REST method
        @type method: str
        @return:
        @rtype: pylastica.response.Response
        """
        data = {'index': data}
        return self.index.request('_settings', method, data)
