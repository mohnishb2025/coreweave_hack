from editor import indent_size

def test_python_indent():
    text = "[*]\nindent_size = 4\n[*.py]\nindent_size = 2\n"
    assert indent_size(text, "foo.py") == 2
