from semver import less_than

def test_numeric_identifiers_and_core_versions():
    assert less_than("1.0.0-alpha.2", "1.0.0-alpha.10") is True
    assert less_than("1.0.0-alpha", "1.0.0-alpha.1") is True
    assert less_than("1.9.0", "1.10.0") is True
    assert less_than("1.0.0-rc.1", "1.0.0") is True
    assert less_than("1.0.0", "1.0.0") is False
