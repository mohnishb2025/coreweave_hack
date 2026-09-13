from email import canonical

def test_plus_tag_is_stripped_from_the_local_part():
    assert canonical("Ada+news@Example.com") == "ada@example.com"
