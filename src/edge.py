class Edge:
    def __init__(self, source, target, attr=None):
        self.source = source
        self.target = target
        self.edge = (source, target)
        if attr is None:
            self.attr = {}
        else:
            self.attr = attr

    def get_id(self):
        return self.edge
