from mailtos import address

def test_plain_and_encoded():
    assert address("mailto:a@b.com") == "a@b.com"
    assert address("mailto:a%40b.com?cc=c") == "a@b.com"
