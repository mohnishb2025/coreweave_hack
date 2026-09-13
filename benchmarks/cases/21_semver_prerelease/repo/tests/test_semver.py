from semver import less_than

def test_prerelease_is_less_than_release():
    assert less_than("1.0.0-alpha", "1.0.0") is True
    assert less_than("1.0.0", "1.0.0-alpha") is False
