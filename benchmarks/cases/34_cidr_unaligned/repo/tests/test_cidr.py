from cidr import contains

def test_slash_12_is_not_the_first_octet():
    assert contains("10.16.0.0/12", "10.31.255.255") is True
    assert contains("10.16.0.0/12", "10.32.0.1") is False
