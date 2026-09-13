from lru import LRU

def test_get_refreshes_recency_before_eviction():
    cache = LRU(2)
    cache.put("a", 1)
    cache.put("b", 2)
    assert cache.get("a") == 1
    cache.put("c", 3)
    assert cache.get("a") == 1
