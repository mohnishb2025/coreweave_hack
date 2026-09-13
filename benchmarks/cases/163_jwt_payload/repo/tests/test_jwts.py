from jwts import claims

def test_unpadded_payload():
    assert claims("x.eyJhIjoxfQ.y") == {"a": 1}
