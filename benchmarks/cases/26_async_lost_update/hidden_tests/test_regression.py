import asyncio
from counter import run

def test_one_and_many_increments():
    assert asyncio.run(run(1)) == 1
    assert asyncio.run(run(8)) == 8
