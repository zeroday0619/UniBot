import requests
import polling

class TwitchStreamAlert:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def oauth2(self):
        url = "https://id.twitch.tv/oauth2/token"
        params = {
            'client_id': f'{self.client_id}',
            'client_secret': f'{self.client_secret}',
            'grant_type': 'client_credentials'
        }
        res = requests.post(url=url, params=params)
        return res.json()['access_token']

    def TwitchApi(self, oauth, name):
        url = "https://api.twitch.tv/helix/" + "users"
        headers = {
            'Authorization': f'Bearer {oauth}'
        }
        params = {
            'login': f'{name}'
        }
        res = requests.get(url=url, headers=headers, params=params).json()['data'][0]['id']
        return res


def is_livestream(response):
    if response == {'data': [], 'pagination': {}}:
        return False
    else:
        return True
class StreamAlert(TwitchStreamAlert):
    def __init__(self, client_id, client_secret):
        super().__init__(client_id, client_secret)
    def main(self, name):    
        url = "https://api.twitch.tv/helix/streams"
        headers = {
            'Client-ID': f'{self.client_id}'
        }
        json = {
            'user_id': f'{self.TwitchApi(oauth=self.oauth2(), name=name)}'
        }
        app = polling.poll(
            lambda: requests.get(url=url, headers=headers, params=json).json(),
            check_success=is_livestream,
            step=5,
            poll_forever=True
        )
        print(app)

# src = StreamAlert(client_id="", client_secret="")
# src.main(name="")