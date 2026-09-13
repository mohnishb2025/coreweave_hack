from weeks import iso_week

def test_january_and_year_end_iso_weeks():
    assert iso_week("2016-01-01") == "2015-W53"
    assert iso_week("2020-12-31") == "2020-W53"
    assert iso_week("2021-01-04") == "2021-W01"
