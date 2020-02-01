import requests
import polling


def is_livestream(response):
    if response == {'data': [], 'pagination': {}}:
        return False
    else:
        return response == response

def oauth2():
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        'client_id': '',
        'client_secret': '',
        'grant_type': 'client_credentials'
    }
    res = requests.post(url=url, params=params)
    return res.json()['access_token']

def TwitchApi():
    url = "https://api.twitch.tv/helix/" + "users"
    headers = {
        'Authorization': f'Bearer {oauth2()}'
    }
    params = {
        'login': ''
    }
    res = requests.get(url=url, headers=headers, params=params).json()['data'][0]['id']
    return res
    
url = "https://api.twitch.tv/helix/streams"
headers = {
    'Client-ID': ''
}
json = {
    'user_id': TwitchApi()
}
app = polling.poll(
    lambda: requests.get(url=url, headers=headers, params=json).json(),
    check_success=is_livestream,
    step=5,
    poll_forever=True
)
print(app)
