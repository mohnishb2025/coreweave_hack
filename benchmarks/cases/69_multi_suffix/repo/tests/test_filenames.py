from filenames import with_suffix

def test_tar_gz_keeps_tar():
    assert with_suffix("archive.tar.gz", ".md") == "archive.tar.md"
