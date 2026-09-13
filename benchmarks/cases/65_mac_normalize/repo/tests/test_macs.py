from macs import normalize

def test_dashes_become_colons():
    assert normalize("AA-BB-CC-DD-EE-FF") == "aa:bb:cc:dd:ee:ff"
