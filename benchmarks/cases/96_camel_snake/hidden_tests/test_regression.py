from snakes import snake

def test_acronyms_and_existing_underscores():
    assert snake("getURL") == "get_url"
    assert snake("XMLParser") == "xml_parser"
    assert snake("already_snake") == "already_snake"
