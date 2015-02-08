import datetime


class SlackEvent(object):
    """Base class for Slack events"""

    def __init__(self, data):
        super(SlackEvent, self).__init__()

        self._raw = data
        self.type = data['type']


class Hello(SlackEvent):
    """Sent when a connection is opened to the message server

    See https://api.slack.com/events/hello for more details
    """

    def __init__(self, data):
        assert data['type'] == 'hello'
        super(Hello, self).__init__(data)


class Message(SlackEvent):
    """Sent when a message is sent to Slack

    See https://api.slack.com/events/message for more details
    """

    def __init__(self, data):
        assert data['type'] == 'message'
        super(Message, self).__init__(data)

        self.subtype = data.get('subtype')
        self.hidden = data.get('hidden', False)
        self.time = datetime.datetime.fromtimestamp(float(data['ts']))

    @property
    def text(self):
        # TODO: Parse the text to make it human readable
        # Currently user mentions look like '<@U03K7341A>' in the text.
        return self._raw['text']

    @property
    def user(self):
        # TODO: Return a user object to make looking up user info easier
        #       and make it lazily loaded
        return self._raw['user']

    @property
    def channel(self):
        # TODO: Return a Channel object to make looking up
        #       channel info easier and it make it lazily loaded
        return self._raw['channel']

    @property
    def team(self):
        # TODO: Return a Team object to make looking up team info
        #       easier and it make it lazily loaded.
        return self._raw['team']

    @property
    def mentioned_users(self):
        """Return a list of users mentioned in the message"""
        raise NotImplementedError


class PresenceChange(SlackEvent):
    """Sent when a user changes status

    See https://api.slack.com/events/presence_change for more details
    """

    def __init__(self, data):
        assert data['type'] == 'presence_change'
        super(PresenceChange, self).__init__(data)

        self.presence = data['presence']

    @property
    def user(self):
        # TODO: Return a user object to make looking up user info easier
        #       and make it lazily loaded
        return self._raw['user']


class UserTyping(SlackEvent):
    """Indicates that the user is currently writing a message to send

    See https://api.slack.com/rtm#typing_indicators for more details
    """

    def __init__(self, data):
        assert data['type'] == 'user_typing'
        super(UserTyping, self).__init__(data)

    @property
    def user(self):
        # TODO: Return a user object to make looking up user info easier
        #       and make it lazily loaded
        return self._raw['user']

    @property
    def channel(self):
        # TODO: Return a Channel object to make looking up
        #       channel info easier and it make it lazily loaded
        return self._raw['channel']


event_mapping = {
    'hello': Hello,
    'message': Message,
    'presence_change': PresenceChange,
    'user_typing': UserTyping
}
