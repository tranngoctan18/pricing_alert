class AlertError(Exception):
    def __init__(self, msg):
        self.message = msg

class TagNameError(AlertError):
    pass

class ReError(AlertError):
    pass