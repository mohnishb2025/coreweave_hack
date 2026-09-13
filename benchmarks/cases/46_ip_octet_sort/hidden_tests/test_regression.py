from ips import sort_ips

def test_cross_octet_numeric_order():
    assert sort_ips(["192.168.1.100", "192.168.1.2"]) == ["192.168.1.2", "192.168.1.100"]
    assert sort_ips(["2.0.0.1", "10.0.0.1"]) == ["2.0.0.1", "10.0.0.1"]
    assert sort_ips(["10.0.0.1"]) == ["10.0.0.1"]
