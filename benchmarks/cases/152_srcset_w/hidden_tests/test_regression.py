from srcsets import pick

def test_smaller_and_exact():
    assert pick("a.jpg 400w, b.jpg 800w", 200) == "a.jpg"
    assert pick("a.jpg 400w, b.jpg 800w", 800) == "b.jpg"
