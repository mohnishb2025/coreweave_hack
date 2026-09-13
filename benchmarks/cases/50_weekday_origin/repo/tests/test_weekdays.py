from weekdays import weekday_name

def test_sunday_is_not_saturday():
    assert weekday_name("2026-09-13") == "Sunday"
