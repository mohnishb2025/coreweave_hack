from etags import same

def test_other_weak_and_mismatch():
    assert same('W/"zz"', '"zz"') is True
    assert same('"abc"', '"xyz"') is False
