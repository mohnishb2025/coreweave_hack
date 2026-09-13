from dmarcs import policy

def test_reject_later_and_quarantine():
    assert policy("v=DMARC1; pct=100; p=reject; rua=mailto:x@y.z") == "reject"
    assert policy("v=DMARC1; p=quarantine; adkim=r") == "quarantine"
