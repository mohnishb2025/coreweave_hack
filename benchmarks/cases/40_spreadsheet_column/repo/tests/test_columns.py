from columns import column_label

def test_column_after_z_uses_two_letters():
    assert column_label(27) == "AA"
