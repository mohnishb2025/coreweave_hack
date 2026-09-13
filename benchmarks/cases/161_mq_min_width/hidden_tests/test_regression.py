from mediaq import min_width

def test_spaces_and_and():
    assert min_width("(min-width:1024px)") == 1024
    assert min_width("(orientation: landscape) and (min-width: 480px)") == 480
