from domains import ascii_host

def test_other_idn_and_plain_hosts():
    assert ascii_host("münchen.de") == "xn--mnchen-3ya.de"
    assert ascii_host("Example.COM") == "example.com"
