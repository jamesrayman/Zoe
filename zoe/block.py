class Block:
    def __init__(self, statements):
        self.statements = statements

    def __len__(self):
        return len(self.statements)

    def __eq__(self, other):
        return self.statements == other.statements

    def __ne__(self, other):
        return self.statements != other.statements

    def repeat(self, times):
        return Block(self.statements * times)

    def extend(self, other):
        return Block(self.statements + other.statements)

    def append(self, statement):
        if not statement.empty():
            self.statements.append(statement)

    def __repr__(self):
        return '\n'.join(str(statement) for statement in self.statements)
