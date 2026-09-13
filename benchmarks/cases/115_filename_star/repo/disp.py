def filename(header):
    return header.split("filename=")[1].split(";")[0].strip().strip('"')
