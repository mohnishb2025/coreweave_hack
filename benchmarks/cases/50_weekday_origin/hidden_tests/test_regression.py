from weekdays import weekday_name

def test_monday_and_known_weekdays():
    assert weekday_name("2026-09-14") == "Monday"
    assert weekday_name("2026-01-01") == "Thursday"
    assert weekday_name("2024-02-29") == "Thursday"
