from jars import samesite

def test_strict_and_default():
    assert samesite("id=1; SameSite=Strict") == "Strict"
    assert samesite("id=1") == "Lax"
