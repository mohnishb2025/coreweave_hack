def require_email(record):
    if "email" not in record:
        raise KeyError("email is required")
    return record["email"]
