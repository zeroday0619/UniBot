import aiohttp
import asyncio

class newApi:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
    
    async def _is_userName(self, oauth, name):
        url = "https://api.twitch.tv/helix/users"
        headers = {
            'Authorization': f'Bearer {oauth}'
        }
        params = {
            'login': f'{name}'
        }

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, params=params) as resp:
                data = await resp.json()
                if resp.status == 200:
                    return data['data'][0]['id']

    async def _is_requests(self, url, headers, params):
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url=url, params=params) as resp:
                data = await resp.json()
                if resp.status == 200:
                    return data

    def is_userName(self, oauth, name):
        data = self.loop.run_until_complete(newApi()._is_userName(oauth, name))
        return data

    def is_requests(self, url, headers, params):
        data = self.loop.run_until_complete(newApi()._is_requests(url, headers, params))
        return data
