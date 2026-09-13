from pager import page_count

def test_partial_page_counts():
    assert page_count(list(range(11)), 10) == 2
