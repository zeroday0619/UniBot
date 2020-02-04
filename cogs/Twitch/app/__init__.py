from .streamAlert import StreamAlert
import time
class alert:
    def __init__(self):
        self.streamAlert = StreamAlert()

    def polling(self, client_id, client_secret, name):
        while True:
            data = self.streamAlert.subscribe(client_id, client_secret, name)
            if self.streamAlert.is_livestream(data):
                return data
            else:
                pass
            time.sleep(30)

