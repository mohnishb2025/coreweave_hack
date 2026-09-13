from etags import same

def test_weak_matches_strong():
    assert same('W/"abc"', '"abc"') is True
