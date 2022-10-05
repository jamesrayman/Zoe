class Symbol:
    def __init__(self, name, index=None):
        if index is None:
            index = []
        self.name = name
        self.index = index

    def __getitem__(self, i):
        return Symbol(self.name, self.index + [i])

    def __eq__(self, other):
        return self.name == other.name and self.index == other.index
