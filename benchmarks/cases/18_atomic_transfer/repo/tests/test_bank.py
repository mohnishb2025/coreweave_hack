import pytest
from bank import transfer

def test_failed_transfer_does_not_debit_source():
    start = {"a": 10, "b": 1}
    with pytest.raises(ValueError, match="insufficient"):
        transfer(start, "a", "b", 15)
    assert start == {"a": 10, "b": 1}
