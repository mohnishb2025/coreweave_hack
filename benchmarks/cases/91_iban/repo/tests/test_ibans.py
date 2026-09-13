from ibans import valid

def test_german_example():
    assert valid("DE89370400440532013000") is True
