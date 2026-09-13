from merge import merge_patch

def test_nested_delete_and_scalar_replacement():
    target = {"user": {"name": "Ada", "city": "Paris"}, "active": True}
    patched = merge_patch(target, {"user": {"city": None}, "active": False})
    assert patched == {"user": {"name": "Ada"}, "active": False}
    assert merge_patch({"keep": 1}, {}) == {"keep": 1}
    assert merge_patch({"x": {"y": 1}}, {"x": 5}) == {"x": 5}
