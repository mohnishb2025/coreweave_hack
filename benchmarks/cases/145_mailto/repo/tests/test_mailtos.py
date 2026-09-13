from mailtos import address

def test_subject_is_not_the_address():
    assert address("mailto:a@b.com?subject=Hi") == "a@b.com"
