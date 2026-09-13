def origin_of(url):
    return url.split("/")[0] + "//" + url.split("/")[2]
