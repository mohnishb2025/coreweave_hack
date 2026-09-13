import pytest
from paths import resolve

def test_parent_escape_is_rejected():
    with pytest.raises(ValueError):
        resolve("/srv/app", "../secret")
