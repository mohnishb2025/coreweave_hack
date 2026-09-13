import asyncio
from lookup import fetch_name

class Client:
    async def get(self, user_id):
        return {"name": f"user-{user_id}"}

def test_second_identifier():
    assert asyncio.run(fetch_name(Client(), 9)) == "user-9"
