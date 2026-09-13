from .cache import CACHE, put

def cached_profile(user_id, loader):
    profile = CACHE.get(user_id)
    if not profile:
        profile = put(user_id, loader(user_id))
    return profile
