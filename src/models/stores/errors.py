

class StoreError(Exception):
    def __init__(self, msg):
        self.msg = msg

class StoreNotFoundError(StoreError):
    pass
