import pytest
from users import require_email

def test_missing_email_is_validation_error():
    with pytest.raises(ValueError, match="email is required"):
        require_email({})
