from mediaq import min_width

def test_tablet_breakpoint():
    assert min_width("(min-width: 768px)") == 768
