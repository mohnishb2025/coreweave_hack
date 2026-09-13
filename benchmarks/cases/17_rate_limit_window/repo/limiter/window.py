def recent(history, now, window):
    return [stamp for stamp in history if now - stamp < window]
