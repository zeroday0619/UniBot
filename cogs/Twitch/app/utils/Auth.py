import aiohttp
import asyncio

class auth:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.url = "https://id.twitch.tv/oauth2/token"


    async def client_credentials(self, client_id, client_secret):
        params = {
            'client_id': f'{client_id}',
            'client_secret': f'{client_secret}',
            'grant_type': 'client_credentials'
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url=self.url, params=params) as resp:
                __client_credentials = await resp.json()
                if resp.status == 200:
                    return __client_credentials['access_token']
    

    def ClientCredentials(self, client_id, client_secret):
        data = self.loop.run_until_complete(auth().client_credentials(client_id, client_secret))
        return data
