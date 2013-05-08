__author__ = 'Joe Linn'

import pylastica.param
#import pylastica.exception

class Script(pylastica.param.Param):
    LANG_MVEL = 'mvel'
    LANG_JS = 'js'
    LANG_GROOVY = 'groovy'
    LANG_PYTHON = 'python'
    LANG_NATIVE = 'native'

    def __init__(self, script, params=None, lang=None):
        """
        @param script: script
        @type script: str
        @param params: script params
        @type params: dict
        @param lang: script language
        @type lang: str
        """
        super(Script, self).__init__()
        self._script = script
        self._lang = lang
        if params is not None:
            assert isinstance(params, dict), "params must be of type dict: %r" % params
            self.params = params

    @property
    def lang(self):
        """
        Get this script's set language
        @return:
        @rtype: str
        """
        return self._lang

    @lang.setter
    def lang(self, lang):
        """
        Set the language for this script
        @param lang: see LANG_* class properties
        @type lang: str
        """
        self._lang = lang

    def set_lang(self, lang):
        """
        Set the language for this script
        @param lang: see LANG_* class properties
        @type lang: str
        @return:
        @rtype: self
        """
        self._lang = lang
        return self

    @property
    def script(self):
        """
        Get the script
        @return:
        @rtype: str
        """
        return self._script

    @script.setter
    def script(self, script):
        """
        Set the script
        @param script:
        @type script: str
        """
        self._script = script

    def set_script(self, script):
        """
        Set the script
        @param script:
        @type script: str
        @return:
        @rtype: self
        """
        self._script = script
        return self

    @classmethod
    def create(cls, data):
        """

        @param cls:
        @type cls: Script
        @param data:
        @type data: str or dict or Script
        @return:
        @rtype: self
        """
        if isinstance(data, Script):
            script = data
        elif isinstance(data, dict):
            script = Script._create_from_dict(data)
        elif isinstance(data, str):
            script = cls(data)
        else:
            raise pylastica.exception.InvalidException("Failed to create script. Invalid data passed: %r" % data)
        return script

    @classmethod
    def _create_from_dict(cls, data):
        """

        @param cls:
        @type cls: Script
        @param data:
        @type data: dict
        @return:
        @rtype: Script
        """
        if 'script' not in data:
            raise pylastica.exception.InvalidException("data['script'] is required.")
        script = cls(data['script'])
        if 'lang' in data:
            script.lang = data['lang']
        if 'params' in data:
            assert isinstance(data['params'], dict), "data['params'] must be a dict: %r" % data['params']
            script.params = data['params']
        return script

    def to_dict(self):
        """

        @return:
        @rtype: dict
        """
        dictionary = {
            'script': self._script
        }
        if len(self._params):
            dictionary['params'] = self._params
        if self._lang is not None:
            dictionary['lang'] = self._lang
        return dictionary
