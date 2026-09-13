from images import split_ref

def test_default_and_registry_port():
    assert split_ref("nginx") == ("nginx", "latest")
    assert split_ref("ex.com:5000/app:2") == ("ex.com:5000/app", "2")
