import asyncio

value = 0


async def bump():
    global value
    current = value
    await asyncio.sleep(0)
    value = current + 1


async def run(count):
    global value
    value = 0
    await asyncio.gather(*[bump() for _ in range(count)])
    return value
