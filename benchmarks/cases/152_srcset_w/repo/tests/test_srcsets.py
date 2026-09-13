from srcsets import pick

def test_picks_the_800w():
    assert pick("a.jpg 400w, b.jpg 800w", 700) == "b.jpg"
