from store import apply
from store.journal import PENDING

def test_commit_applies_once_and_clears():
    PENDING.clear()
    result = apply({"n": 1}, "ok", {"n": 4}, True)
    assert result == {"n": 4}
    assert PENDING == {}
    later = apply({"n": 4}, "ok", {"n": 5}, True)
    assert later == {"n": 5}
