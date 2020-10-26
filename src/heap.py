class Node(object):
    def __init__(self, ident, astobj):
        self.ident = ident
        self.left = None
        self.right = None
        if astobj is type(ASTObject):
            self.astobj = astobj
        else:
            raise AssertionError("Error: cannot push item to heap. Item is not an AST Object.")

    def insert(self, ident, astobj):
        if self.astobj:
            if ident < self.ident:
                if self.left is None:
                    self.left = Node(ident, astobj)
                else:
                    self.left.insert(ident, astobj)
            elif ident > self.ident:
                if self.right is None:
                    self.right = Node(ident, astobj)
                else:
                    self.right.insert(ident, astobj)
        else:
            self.astobj = astobj
            self.ident = ident
