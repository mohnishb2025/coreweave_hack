from merge import deep_merge

def test_nested_mutation_does_not_change_input():
    base = {"a": {"x": 1}, "b": 2}
    result = deep_merge(base, {"a": {"y": 3}})
    result["a"]["x"] = 99
    assert base["a"]["x"] == 1
    assert result["a"]["y"] == 3
