__author__ = 'Joe Linn'

#import pylastica
import pylastica.response

class ResponseSet(pylastica.response.Response):
    def __init__(self, response, bulk_responses):
        """

        @param response:
        @type response: pylastica.response.Response
        @param bulk_responses:
        @type bulk_responses: list of pylastica.bulk.response.Response
        """
        super(ResponseSet, self).__init__(response.data)
        self._bulk_responses = bulk_responses

    @property
    def bulk_responses(self):
        """

        @return:
        @rtype: list of pylastica.bulk.response.Response
        """
        return self._bulk_responses

    def get_error(self):
        """
        Returns the first found error
        @return:
        @rtype: self
        """
        error = ''
        for response in self.bulk_responses:
            if response.has_error():
                error = response.get_error()
                break
        return error

    @property
    def error(self):
        """

        @return:
        @rtype: str
        """
        return self.get_error()

    def is_ok(self):
        """

        @return:
        @rtype: bool
        """
        ret = True
        for response in self.bulk_responses:
            if not response.is_ok():
                ret = False
                break
        return ret

    def has_error(self):
        """

        @return:
        @rtype: bool
        """
        ret = False
        for response in self.bulk_responses:
            if response.has_error():
                ret = True
                break
        return ret

    def __iter__(self):
        return iter(self.bulk_responses)

    def __len__(self):
        """

        @return:
        @rtype: int
        """
        return len(self.bulk_responses)

    def __getitem__(self, item):
        """

        @param item:
        @type item: int
        @return:
        @rtype: pylastica.bulk.response.Response
        """
        return self.bulk_responses[item]
