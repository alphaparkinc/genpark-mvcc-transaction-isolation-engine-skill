"""Multi-Version Concurrency Control (MVCC) Engine
100% Python Standard Library.
"""

class MVCCEngine:
    """Snapshot isolation tuple versioning manager."""
    def __init__(self):
        self.global_tx_id = 1
        self.store = {}

    def begin_transaction(self):
        tx_id = self.global_tx_id
        self.global_tx_id += 1
        return tx_id

    def write(self, tx_id, key, value):
        if key not in self.store:
            self.store[key] = []
        for i in range(len(self.store[key])):
            val, xmin, xmax = self.store[key][i]
            if xmax is None:
                self.store[key][i] = (val, xmin, tx_id)
        self.store[key].append((value, tx_id, None))

    def read(self, tx_id, key):
        if key not in self.store:
            return None
        for val, xmin, xmax in reversed(self.store[key]):
            if xmin <= tx_id:
                if xmax is None or xmax > tx_id:
                    return val
        return None
