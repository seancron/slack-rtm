import json

import requests
import websocket

from .events import event_mapping, SlackEvent
from .exceptions import SlackConnectionError

class SlackRTMClient(object):
    BASE_API_URL = 'https://slack.com/api/{method}'

    def __init__(self, token):
        self.token = token
        self.websocket = None

    def _start(self):
        response = requests.get(self.BASE_API_URL.format(method='rtm.start'),
                                params={'token': self.token})

        if response.status_code != 200:
            raise SlackConnectionError("Failed to connect. Returned {} status code".format(response.status_code))

        data = response.json()
        if not data['ok']:
            raise SlackConnectionError("Could not start RTM connection")

        return data

    def connect(self):
        """Establish a websocket connection with Slack

        By default it creates a non-blocking socket.
        Use `set_timeout` to change this behavior.
        """
        data = self._start()
        self.websocket = websocket.create_connection(data['url'])
        self.set_timeout(0)

    def set_timeout(self, timeout):
        """Set the timeout for the websocket"""
        self.websocket.sock.settimeout(timeout)

    def read(self):
        """Read a message from the websocket"""
        try:
            while True:
                data = self.websocket.recv()
                event = self.process_event(data)
                yield event
        except Exception as e:
            # TODO: Raise more specific exceptions when socket is disconnected
            #       or there are other issues with reading messages
            raise StopIteration(str(e))

    @staticmethod
    def process_event(event):
        """Returns an Event object"""

        event = json.loads(event)
        event_type = event['type']

        if event_type in event_mapping:
            return event_mapping[event_type](event)
        else:
            return SlackEvent(event)
