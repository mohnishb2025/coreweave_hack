from perms import camera

def test_self_and_missing():
    assert camera("CAMERA=(self)") is True
    assert camera("geolocation=(self)") is False
