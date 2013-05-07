__author__ = 'Joe Linn'

#import pylastica
import pylastica.response

class Response(pylastica.response.Response):
    def __init__(self, response_data, action, op_type):
        """

        @param response_data:
        @type response_data: dict or str
        @param action:
        @type action: pylastica.bulk.action.Action
        @param op_type: bulk operation type
        @type op_type: str
        """
        assert isinstance(action, pylastica.bulk.action.Action), "action must be an instance of Action: %r" % action
        super(Response, self).__init__(response_data)
        self._action = action
        self._op_type = op_type

    @property
    def action(self):
        """

        @return:
        @rtype: pylastica.bulk.action.Action
        """
        return self._action

    @property
    def op_type(self):
        """

        @return:
        @rtype: str
        """
        return self._op_type
