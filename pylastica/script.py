__author__ = 'Joe Linn'

import pylastica.param


class Script(pylastica.param.Param):
    LANG_MVEL = 'mvel'
    LANG_JS = 'js'
    LANG_GROOVY = 'groovy'
    LANG_PYTHON = 'python'
    LANG_NATIVE = 'native'

    def __init__(self, script, params=None, lang=None, doc_id=None):
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
        self._upsert = None
        if params is not None:
            assert isinstance(params, dict), "params must be of type dict: %r" % params
            self.params = params
        if doc_id is not None:
            self.doc_id = doc_id

    @property
    def upsert(self):
        """

        @return:
        @rtype: pylastica.document.Document
        """
        return self._upsert

    @upsert.setter
    def upsert(self, data):
        """

        @param data:
        @type data: dict or pylastica.document.Document
        """
        document = pylastica.document.Document.create(data)
        self._upsert = document

    def has_upsert(self):
        """

        @return:
        @rtype: bool
        """
        return self._upsert is not None

    @property
    def doc_id(self):
        """

        @return:
        @rtype: str
        """
        return self.get_param('_id') if self.has_param('_id') else None

    @doc_id.setter
    def doc_id(self, doc_id):
        """

        @param doc_id:
        @type doc_id: str
        """
        self.set_param('_id', doc_id)

    def has_doc_id(self):
        """

        @return:
        @rtype: bool
        """
        return self.has_param('_id')

    def get_options(self, fields=None, with_underscore=False):
        """

        @param fields: if None, all options will be returned. Field names can be with or without underscores. (_percolate, routing)
        @type fields: list of str
        @param with_underscore: if true, option keys should contain an underscore prefix
        @type with_underscore: bool
        @return:
        @rtype: dict
        """
        def strip_underscore(string):
            if not with_underscore:
                return string.lstrip('_')
            return string

        if fields is not None:
            data = {}
            for field in fields:
                key = '_' + field.lstrip('_')
                if self.has_param(key) and str(self.get_param(key)) != '':
                    data[strip_underscore(key)] = self.get_param(key)
        else:
            data = {strip_underscore(key): value for key, value in self.params.iteritems()}
        return data

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
