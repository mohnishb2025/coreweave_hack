from merge import deep_merge

def test_lists_and_identity_are_copied():
    base = {"items": [1, 2], "keep": {"z": 1}}
    result = deep_merge(base, {"extra": True})
    result["items"].append(3)
    result["keep"]["z"] = 8
    assert base["items"] == [1, 2]
    assert base["keep"] == {"z": 1}
    assert result is not base
    assert "extra" not in base
