"""
# Twitch Live Stream Alert
## developer : zeroday0619
-------------------------------------------------
(C)2020. Team Uni All Rights Reserved
"""
import asyncio
import aiohttp
import polling
import time
import ujson

def is_livestream(response):
    if response == {'data': [], 'pagination': {}}:
        return False
    else:
        return True

class TwitchStreamAlert:
    def __init__(self):
        self.loop = asyncio.get_event_loop()

    async def oauth2(self, client_id, client_secret):
        url = "https://id.twitch.tv/oauth2/token"
        params = {
            'client_id': f'{client_id}',
            'client_secret': f'{client_secret}',
            'grant_type': 'client_credentials'
        }
        async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
            async with session.post(url=url, json=params) as resp:
                rp = await resp.json()
            return rp['access_token']
        

    async def TwitchApi(self, oauth, name):
        url = "https://api.twitch.tv/helix/" + "users"
        headers = {
            'Authorization': f'Bearer {oauth}'
        }
        params = {
            'login': f'{name}'
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url=url, params=params) as resp:
                rp = await resp.json()
            return rp['data'][0]['id']

    async def is_requests(self, url, headers, params):
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url=url, params=params) as resp:
                rp = await resp.json()
            return rp

class StreamAlert:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.echo = TwitchStreamAlert()


    async def ATLSA(self, name, client_id, client_secret):

        url = "https://api.twitch.tv/helix/streams"
        headers = {
            'Client-ID': f'{client_id}'
        }
        oauth = await self.echo.oauth2(client_id, client_secret)
        twitchapi = await self.echo.TwitchApi(oauth=oauth, name=name)
        json = {
            'user_id': f'{twitchapi}'
        }
        req = await self.echo.is_requests(url=url, headers=headers, params=json)
        return req

async def main():
    loop = asyncio.get_event_loop()
    app = StreamAlert()

    while True:
        time.sleep(0.5*2)
        val = await app.ATLSA(name="",client_id="", client_secret="")
        if is_livestream(val):
            print(val)
            return val
        else:
            pass
asyncio.run(main())