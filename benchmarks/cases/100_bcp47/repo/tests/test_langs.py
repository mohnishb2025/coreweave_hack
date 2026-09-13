from langs import canonical

def test_region_stays_upper():
    assert canonical("en-US") == "en-US"
