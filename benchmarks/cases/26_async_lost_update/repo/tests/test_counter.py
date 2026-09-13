import asyncio
from counter import run

def test_concurrent_increments_are_not_lost():
    assert asyncio.run(run(20)) == 20
