from config import load_flag

def test_false_string():
    assert load_flag({"FEATURE": "false"}, "FEATURE") is False
