class Node(object):
    def __init__(self, identifier, ast_obj, left, right):        
        self.identifier = identifier
        self.left = left
        self.right = right
        self.ast_obj = ast_obj

    def insert(self, value, ast_obj):        
        if value <= self.identifier:
            if not (self.left == None):
                self.left.insert(value, ast_obj)
            else:
                self.left = Node(value, ast_obj, None, None)                  
        elif value >= self.identifier:
            if not (self.right == None):
                self.right.insert(value, ast_obj)
            else:                
                self.right = Node(value, ast_obj, None, None)                

    def search(self, indentifier):          
        if self.identifier == indentifier:             
            return self

        if self.identifier < indentifier: 
            if not (self.left == None):
                self.left.search(indentifier)
        
        if self.identifier > indentifier:            
            if not (self.right == None):
                self.right.search(indentifier)
            
    def __str__(self):
        return str(self.identifier)
