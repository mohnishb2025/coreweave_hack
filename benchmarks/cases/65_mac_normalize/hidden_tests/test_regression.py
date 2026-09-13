from macs import normalize

def test_compact_and_mixed_separators():
    assert normalize("AABBCCDDEEFF") == "aa:bb:cc:dd:ee:ff"
    assert normalize("Aa:Bb-Cc:Dd-Ee:Ff") == "aa:bb:cc:dd:ee:ff"
