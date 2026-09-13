from hosts import same_host

def test_zero_compression_and_case():
    assert same_host("2001:db8::1", "2001:0db8:0000:0000:0000:0000:0000:0001") is True
    assert same_host("2001:DB8::1", "2001:db8:0:0:0:0:0:1") is True
    assert same_host("2001:db8::1", "2001:db8::2") is False
