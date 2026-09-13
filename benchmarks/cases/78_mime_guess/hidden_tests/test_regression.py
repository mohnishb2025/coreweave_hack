from mimes import mime_type

def test_jpeg_png_and_html():
    assert mime_type("a.jpeg") == "image/jpeg"
    assert mime_type("a.PNG") == "image/png"
    assert mime_type("index.HTML") == "text/html"
