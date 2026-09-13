from params import get_all

def test_plus_and_order():
    assert get_all("q=a+b&q=c", "q") == ["a b", "c"]
    assert get_all("b=9&a=1", "a") == ["1"]
