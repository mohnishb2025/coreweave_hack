import asyncio
from retry import retry

def test_retries_means_extra_attempts():
    attempts = 0
    async def operation():
        nonlocal attempts
        attempts += 1
        if attempts < 2:
            raise RuntimeError("temporary")
        return "ok"
    assert asyncio.run(retry(operation, retries=1)) == "ok"
