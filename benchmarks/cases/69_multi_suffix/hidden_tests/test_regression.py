from filenames import with_suffix

def test_other_compound_and_extensionless():
    assert with_suffix("bundle.tar.gz", ".zip") == "bundle.tar.zip"
    assert with_suffix("README", ".md") == "README.md"
    assert with_suffix("notes.txt", ".md") == "notes.md"
