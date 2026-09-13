from pathlib import PurePosixPath

def resolve(root, relative):
    return str(PurePosixPath(root) / relative)
