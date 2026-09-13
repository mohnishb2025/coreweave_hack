from ini import get

def test_dev_and_name():
    text = "[prod]\nport=80\nname=p\n[dev]\nport=8000\nname=d\n"
    assert get(text, "dev", "port") == "8000"
    assert get(text, "prod", "name") == "p"
