from bank import transfer

def test_successful_transfer_does_not_alias_input():
    start = {"a": 10, "b": 1}
    result = transfer(start, "a", "b", 4)
    assert result == {"a": 6, "b": 5}
    assert start == {"a": 10, "b": 1}
    assert result is not start
