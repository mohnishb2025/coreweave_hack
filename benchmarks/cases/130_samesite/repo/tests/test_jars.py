from jars import samesite

def test_none_is_explicit():
    assert samesite("id=1; SameSite=None; Secure") == "None"
