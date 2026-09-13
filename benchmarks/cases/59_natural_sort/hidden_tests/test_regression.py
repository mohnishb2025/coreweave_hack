from labels import sort_names

def test_split_numeric_runs_and_ties():
    assert sort_names(["img10.png", "img2.png", "img2a.png"]) == [
        "img2.png",
        "img2a.png",
        "img10.png",
    ]
    assert sort_names(["a10", "a2", "a1"]) == ["a1", "a2", "a10"]
