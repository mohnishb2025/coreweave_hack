from weeks import iso_week

def test_late_december_can_belong_to_next_iso_year():
    assert iso_week("2018-12-31") == "2019-W01"
