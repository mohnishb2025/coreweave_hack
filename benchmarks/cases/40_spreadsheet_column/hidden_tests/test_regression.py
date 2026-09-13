from columns import column_label

def test_wraps_through_az_and_aaa():
    assert column_label(1) == "A"
    assert column_label(26) == "Z"
    assert column_label(52) == "AZ"
    assert column_label(53) == "BA"
    assert column_label(702) == "ZZ"
    assert column_label(703) == "AAA"
