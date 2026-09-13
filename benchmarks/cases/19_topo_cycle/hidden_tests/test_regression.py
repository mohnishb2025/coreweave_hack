from schedule import order

def test_diamond_dependencies_keep_prereqs_first():
    result = order({"d": ["b", "c"], "b": ["a"], "c": ["a"], "a": []})
    assert result.index("a") < result.index("b")
    assert result.index("a") < result.index("c")
    assert result.index("b") < result.index("d")
    assert result.index("c") < result.index("d")
