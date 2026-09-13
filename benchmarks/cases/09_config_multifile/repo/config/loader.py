from .parser import parse_bool

def load_flag(env, name, default=False):
    return parse_bool(env[name]) if name in env else default
