import aiohttp

async def post_to_api(endpoint, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(endpoint, json=data) as response:
            return response.status, await response.json()