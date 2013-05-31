__author__ = 'Joe Linn'

import json
import logging


class Log(object):
    def __init__(self, log=''):
        """
        @param log: file name for logging
        @type log: str
        """
        super(Log, self).__init__()
        self._log = True #log path or True if enabled
        self._last_message = ''
        self.set_log(log)

    def log(self, level, message, context=None):
        """

        @param level: log level
        @type level: str
        @param message: message to log
        @type message: str
        @param context:
        @type context: dict
        @return:
        @rtype: void
        """
        if context is None:
            context = {}
        context['error_message'] = message
        self._last_message = json.dumps(context)
        logging.log(level, message)

    def set_log(self, log):
        """
        Enable / disable logging or set log path
        @param log: enables logging or sets the log path
        @type log: bool or str
        @return:
        @rtype: self
        """
        self._log = log
        if isinstance(log, str):
            #set log file
            logging.basicConfig(filename=log)
        return self

    @property
    def last_message(self):
        """

        @return:
        @rtype: str
        """
        return self._last_message
