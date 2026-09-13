from .journal import drop, prepare, take

def apply(db, tx_id, writes, commit):
    prepare(tx_id, writes)
    if not commit:
        drop(tx_id)
        return dict(db)
    result = dict(db)
    result.update(take(tx_id))
    return result
