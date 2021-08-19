class DotData:
    enabled = False
    def __init__(self, name, relative_path, status):
        self.name = name
        self.relative_path = relative_path
        self.status = status
    def set_status(self, status):
        self.status = status
