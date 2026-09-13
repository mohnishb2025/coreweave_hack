import pytest
from average import mean

def test_empty_list_is_a_value_error():
    with pytest.raises(ValueError, match="empty"):
        mean([])
