import asyncio
from lookup import fetch_name

class Client:
    async def get(self, user_id):
        return {"name": f"user-{user_id}"}

def test_fetch_name_awaits_client():
    assert asyncio.run(fetch_name(Client(), 7)) == "user-7"
