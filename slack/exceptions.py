class SlackException(Exception):
    pass

class SlackConnectionError(SlackException):
    pass

class SlackReadError(SlackException):
    pass
