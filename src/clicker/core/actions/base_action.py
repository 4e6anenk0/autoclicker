class BaseAction:
    def __init__(self):
        self.name = __class__.__name__

    def configure(self):
        pass

    def execute(self, **kwars):
        pass