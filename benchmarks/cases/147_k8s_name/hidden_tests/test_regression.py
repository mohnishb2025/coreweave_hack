from kube import valid

def test_underscore_and_ok():
    assert valid("my_pod") is False
    assert valid("my-pod") is True
