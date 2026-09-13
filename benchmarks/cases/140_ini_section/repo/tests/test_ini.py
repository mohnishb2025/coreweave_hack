from ini import get

def test_prod_port():
    text = "[prod]\nport=80\n[dev]\nport=8000\n"
    assert get(text, "prod", "port") == "80"
