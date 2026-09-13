from store import apply
from store.journal import PENDING

def test_abort_clears_prepared_writes():
    PENDING.clear()
    result = apply({"n": 1}, "tx", {"n": 9}, False)
    assert result == {"n": 1}
    assert PENDING == {}
