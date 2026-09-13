from editor import indent_size

def test_md_and_star():
    text = "[*]\nindent_size = 4\n[*.py]\nindent_size = 2\n[*.md]\nindent_size = 2\n"
    assert indent_size(text, "README.md") == 2
    assert indent_size(text, "app.js") == 4
