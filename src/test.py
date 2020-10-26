from node import *
from astclasses import *

tree = Node(0, ASTObject("x", 1), None, None)

for i in range(1,10,1):
    tree.insert(i, ASTObject("x", 1))     

print(tree.search(0))
print(tree.search(1))