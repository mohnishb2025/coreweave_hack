from hosts import same_host

def test_loopback_compressed_matches_expanded():
    assert same_host("::1", "0:0:0:0:0:0:0:1") is True
