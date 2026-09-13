from perms import camera

def test_empty_allowlist_denies():
    assert camera("camera=(), geolocation=(self)") is False
