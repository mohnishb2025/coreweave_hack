from cidr import contains

def test_exact_host_and_half_octet_masks():
    assert contains("192.168.1.0/24", "192.168.1.50") is True
    assert contains("192.168.1.0/24", "192.168.2.1") is False
    assert contains("192.168.1.0/25", "192.168.1.200") is False
    assert contains("10.0.0.1/32", "10.0.0.1") is True
    assert contains("10.0.0.1/32", "10.0.0.2") is False
