import pytest
from lru import LRU

def test_put_of_existing_key_refreshes_and_updates():
    cache = LRU(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("a", 9)
    cache.put("c", 3)
    assert cache.get("a") == 9
    with pytest.raises(KeyError):
        cache.get("b")
