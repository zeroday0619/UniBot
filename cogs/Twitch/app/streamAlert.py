from .utils import headers_client_id
from .utils import params_user_id
from .utils import api
from .utils import auth

class StreamAlert:
    def __init__(self):
        self.subscribeUrl = "https://api.twitch.tv/helix/streams"
        self.api = api()
        self.auth = auth()

    def is_livestream(self, response):
        if response == {'data': [], 'pagination': {}}:
            return False
        else:
            return True
    
    def subscribe(self, client_id, client_secret, name):
        token = self.auth.ClientCredentials(client_id=client_id, client_secret=client_secret)
        user_id = self.api.is_userName(oauth=token, name=name)

        headers = headers_client_id(client_id=client_id)
        params = params_user_id(user_id=user_id)
        
        req = self.api.is_requests(url=self.subscribeUrl, headers=headers, params=params)
        return req