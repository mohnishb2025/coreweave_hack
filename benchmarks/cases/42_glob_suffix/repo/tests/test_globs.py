from globs import match

def test_star_txt_does_not_match_backup_suffix():
    assert match("notes.txt", "*.txt") is True
    assert match("notes.txt.bak", "*.txt") is False
