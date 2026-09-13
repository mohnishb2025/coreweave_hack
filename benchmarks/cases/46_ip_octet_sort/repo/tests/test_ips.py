from ips import sort_ips

def test_tenth_address_is_after_the_second():
    assert sort_ips(["10.0.0.2", "10.0.0.10"]) == ["10.0.0.2", "10.0.0.10"]
