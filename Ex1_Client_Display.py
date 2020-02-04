import requests
import threading
import json


class HubClient(object):
    def __init__(self, url):
        self._url = url
        self._ignore = set()

    def _connect(self):
        self._active = True
        next_frame_id = -1
        while self._active:
            frames = requests.get(self._url, params = {"since": str(next_frame_id)}).json()
            for (frame_id, payload) in frames:
                next_frame_id = frame_id + 1
                if frame_id in self._ignore:
                    self._ignore.remove(frame_id)
                else:
                    self.handle_frame(payload)

    def connect(self, blocking = True):
        if blocking:
            self._connect()
        else:
            threading.Thread(target = self._connect).start()

    def handle_frame(self, payload):
        try:
            print(json.loads(payload))
        except:
            print(payload)

    def send(self, payload):
        frame_id = requests.post(self._url, data = {"frame": payload}).json()
        self._ignore.add(frame_id)

    def disconnect(self):
        self._active = False

__all__ = ["HubClient"]


def main():
    displayClient = HubClient("http://mxg.together.org.il/hub")
    displayClient.connect(False)
    displayClient.send("Display Client is UP")


if __name__ == '__main__':
    main()