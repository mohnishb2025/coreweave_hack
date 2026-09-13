from versions import same

def test_missing_patch_is_zero():
    assert same("1.2", "1.2.0") is True
