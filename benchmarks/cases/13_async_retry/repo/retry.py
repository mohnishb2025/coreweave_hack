async def retry(operation, retries):
    for _ in range(retries):
        try:
            return await operation()
        except RuntimeError:
            pass
    raise RuntimeError("exhausted")
