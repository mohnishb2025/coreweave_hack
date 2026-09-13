import pytest
from paths import resolve

def test_absolute_and_normalized_escapes():
    with pytest.raises(ValueError):
        resolve("/srv/app", "/etc/passwd")
    with pytest.raises(ValueError):
        resolve("/srv/app", "foo/../../etc/passwd")
    assert resolve("/srv/app", "ok/file.txt") == "/srv/app/ok/file.txt"
    assert resolve("/srv/app", "./nested") == "/srv/app/nested"
