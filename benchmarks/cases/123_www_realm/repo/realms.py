def realm(header):
    return header.split("realm=")[1].strip('"')
