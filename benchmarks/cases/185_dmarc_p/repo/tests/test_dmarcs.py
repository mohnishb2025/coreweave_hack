from dmarcs import policy

def test_none_with_rua():
    assert policy("v=DMARC1; p=none; rua=mailto:a@b.com") == "none"
