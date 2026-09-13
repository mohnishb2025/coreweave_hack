from .window import recent

def accept(history, now, limit, window):
    history.append(now)
    return len(recent(history, now, window)) <= limit
