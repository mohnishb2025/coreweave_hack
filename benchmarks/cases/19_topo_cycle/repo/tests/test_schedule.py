import pytest
from schedule import order

def test_cycle_is_an_error():
    with pytest.raises(ValueError, match="cycle"):
        order({"build": ["test"], "test": ["build"]})
