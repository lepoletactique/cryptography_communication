import requests
import threading

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
        print(payload)

    def send(self, payload):
        frame_id = requests.post(self._url, data = {"frame": payload}).json()
        self._ignore.add(frame_id)

    def disconnect(self):
        self._active = False

__all__ = ["HubClient"]


def main():
    print("starting stuff")
    hub = HubClient("http://mxg.together.org.il/hub")
    hub.connect(False)
    print("connected")
    hub.send("Hayeladim Shotim")

if __name__ == "__main__":
    main()