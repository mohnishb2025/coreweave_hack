from config import load_flag

def test_zero_string():
    assert load_flag({"FEATURE": "0"}, "FEATURE") is False
