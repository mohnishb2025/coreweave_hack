from paths import replace_extension

def test_dotted_directory_and_filename():
    assert replace_extension("archive.v1/report.final.txt", "json") == "archive.v1/report.final.json"
