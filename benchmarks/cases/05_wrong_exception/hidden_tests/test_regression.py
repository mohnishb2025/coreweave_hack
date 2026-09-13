import pytest
from users import require_email

def test_error_is_not_mapping_leak():
    with pytest.raises(ValueError):
        require_email({"name": "Ada"})
