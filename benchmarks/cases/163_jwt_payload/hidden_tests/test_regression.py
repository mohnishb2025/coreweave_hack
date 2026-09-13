from jwts import claims

def test_other_unpadded_and_urlsafe():
    assert claims("x.eyJhZG1pbiI6dHJ1ZX0.y") == {"admin": True}
    assert claims("x.eyJ1IjoiYV9iIn0.y")["u"] == "a_b"
