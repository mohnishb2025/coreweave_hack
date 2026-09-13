import asyncio
from retry import retry

def test_zero_retries_still_attempts_once():
    async def operation():
        return 42
    assert asyncio.run(retry(operation, retries=0)) == 42
