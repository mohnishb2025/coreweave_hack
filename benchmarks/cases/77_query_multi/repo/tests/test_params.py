from params import get_all

def test_repeated_key_keeps_both():
    assert get_all("a=1&a=2", "a") == ["1", "2"]
