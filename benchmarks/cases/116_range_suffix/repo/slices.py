def slice_start(length, spec):
    return int(spec.split("-")[0].split("=")[-1] or 0)
