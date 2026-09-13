PENDING = {}

def prepare(tx_id, writes):
    PENDING[tx_id] = dict(writes)

def drop(tx_id):
    return None

def take(tx_id):
    return PENDING[tx_id]
