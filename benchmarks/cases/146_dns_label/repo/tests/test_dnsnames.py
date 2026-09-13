from dnsnames import valid

def test_underscore_is_invalid():
    assert valid("_svc") is False
