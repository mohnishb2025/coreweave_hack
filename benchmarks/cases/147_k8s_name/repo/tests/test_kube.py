from kube import valid

def test_uppercase_is_invalid():
    assert valid("MyPod") is False
