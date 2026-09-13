def contains(cidr, ip):
    network, prefix = cidr.split("/")
    keep = int(prefix) // 8
    stem = ".".join(network.split(".")[:keep])
    return ip.startswith(stem)
