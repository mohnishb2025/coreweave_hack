from pager import page_count

def test_single_partial_page():
    assert page_count([1], 10) == 1
