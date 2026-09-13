from mimes import mime_type

def test_uppercase_jpeg_extension():
    assert mime_type("X.JPG") == "image/jpeg"
