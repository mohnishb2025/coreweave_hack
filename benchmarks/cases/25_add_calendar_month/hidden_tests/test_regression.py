from datetime import date
from months import add_months

def test_leap_day_and_month_end_clipping():
    assert add_months(date(2020, 1, 31), 1) == date(2020, 2, 29)
    assert add_months(date(2019, 3, 31), 1) == date(2019, 4, 30)
    assert add_months(date(2019, 12, 31), 1) == date(2020, 1, 31)
    assert add_months(date(2019, 1, 15), 1) == date(2019, 2, 15)
