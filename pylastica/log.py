__author__ = 'Joe Linn'

import pylastica

class Log(object):
    def __init__(self):
        self._log = True #log path or True if enabled
        self._last_message = ''
        super(Log, self).__init__()

    def log(self, message):
        if isinstance(message, pylastica.Request):
            message = str(message)
        self._last_message = message
        if self._log is not None and isinstance(self._log, str):
            #TODO: logging stuff
            pass

    def set_log(self, log):
        """
        Enable / disable logging or set log path
        @param log: enables logging or sets the log path
        @type log: bool or str
        @return:
        @rtype: self
        """
        self._log = log
        return self

    @property
    def last_message(self):
        """

        @return:
        @rtype: str
        """
        return self._last_message
