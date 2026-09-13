from realms import realm

def test_unquoted_and_bearer():
    assert realm("Bearer realm=simple, extra=1") == "simple"
    assert realm('Basic realm="only"') == "only"
