from std import *
from astclasses import *
from heap import *
from rply import ParserGenerator, LexerGenerator
from rply.token import BaseBox


# Memory management
stack = []
# @todo(tdamron): Implement a better data structure for the heap. Searching this for ASTObjects is O(n). BST could be O(log n).
# @todo(tdamron): The heap needs a garbage collector... or does it?
# heap = Node(0, None, None, None)
heap = []

def get_stack():
    return stack

def get_heap():
    return heap

'''
LEXER
'''

lg = LexerGenerator()

# todo(tdamron): Add list support for multiple elements in the list
lg.add("PLUS", r"\+")
lg.add("MINUS", r"\-")
lg.add("MULTIPLY", r"\*")
lg.add("INTDIV", r"\/")
lg.add("FLOAT", r"\d+\.\d+")
lg.add("INT", r"\d+")
lg.add("STRING", r'".+"')
lg.add("BOOL", r"(?:True|False)")
lg.add("SEMICLN", r";")
lg.add("IDENT", r"\w+")
lg.add("LPAREN", r"\(")
lg.add("RPAREN", r"\)")
lg.add("VAREQ", r":=")
lg.add("LISTSTART", r"\[")
lg.add("LISTEND", r"\]")
lg.add("COMMA", r"\,")

lg.ignore(r"\s+")

'''
PARSER
'''

pg = ParserGenerator(["INT", "FLOAT", "STRING", "BOOL", "PLUS", "MINUS", "MULTIPLY", "INTDIV", "SEMICLN", "LPAREN", "RPAREN", "IDENT", "VAREQ", "LISTSTART", "LISTEND", "COMMA"], cache_id="tusk")

@pg.production("statement : expr SEMICLN")
@pg.production("statement : func SEMICLN")
def statement(p):
    return p[0]

# @todo(tdamron): Implement "for" function (may want to update heap first).
@pg.production("func : IDENT LPAREN expr RPAREN")
def func(p):
    if p[0].getstr() == "put":
        put = Put([Variable("x", str(p[2]))])
        stack.append(put)
    elif p[0].getstr() == "poke":
        poke = Poke([Variable("x", str(p[2]))], heap)
        stack.append(poke)
    elif p[0].getstr() == "pop":
        pop = Pop([Variable("x", str(p[2]))], heap)
        stack.append(pop)        
    elif p[0].getstr() == "for":
        # Args :: name -> function to perform -> list of items
        fr = For("for", "", "")


@pg.production("func : IDENT LPAREN  RPAREN")
def func(p):    
    if p[0].getstr() == "dump":
        dump = Dump(heap)
        stack.append(dump)
    if p[0].getstr() == "peak":
        peak = Peak(heap)
        stack.append(peak)

@pg.production("expr : LPAREN expr PLUS expr RPAREN")
@pg.production("expr : LPAREN expr MINUS expr RPAREN")
@pg.production("expr : LPAREN expr INTDIV expr RPAREN")
@pg.production("expr : LPAREN expr MULTIPLY expr RPAREN")
def expr_paren_op(p):
    lhs = p[1]
    rhs = p[3]
    if p[2].gettokentype() == "PLUS":
        return lhs + rhs
    elif p[2].gettokentype() == "MINUS":
        return lhs - rhs
    elif p[2].gettokentype() == "MULTIPLY":
        return lhs * rhs
    elif p[2].gettokentype() == "INTDIV":
        return lhs / rhs
    else:
        print("This should not happen. If you are seeing this message, it may be the apocalypse.")
        
@pg.production("expr : expr PLUS expr")
@pg.production("expr : expr MINUS expr")
@pg.production("expr : expr MULTIPLY expr")
@pg.production("expr : expr INTDIV expr")
def expr_op(p):
    lhs = p[0]
    rhs = p[2]
    if p[1].gettokentype() == "PLUS":
        return lhs + rhs
    elif p[1].gettokentype() == "MINUS":
        return lhs - rhs
    elif p[1].gettokentype() == "MULTIPLY":
        return lhs * rhs
    elif p[1].gettokentype() == "INTDIV":
        return lhs / rhs
    else:
        print("Error.")

@pg.production("expr : INT")
def expr_num(p):    
    return int(p[0].getstr())

@pg.production("expr : FLOAT")
def expr_float(p):
    return float(p[0].getstr())

# @todo(tdamron): Tusk should support escape sequences... why doesn't it just work?
@pg.production("expr : STRING")
def expr_string(p):
    string = ""
    for char in p[0].getstr():
        if not char == "\"":
            string += char    
    return string

@pg.production("expr : BOOL")
def expr_bool(p):
    b = p[0]
    if b.getstr() == "True":
        return True
    elif b.getstr() == "False":
        return False

@pg.production("expr : MINUS INT")
def expr_negative(p):
    return -1 * int(p[1].getstr())

# This would be used to access variables from the heap.
@pg.production("expr : IDENT")
def expr_ident(p):
    ident = p[0].getstr()
    for obj in reversed(heap):
        if obj.name == ident:
            return obj.value

    raise AssertionError("Error: %s not found." % ident)

@pg.production("expr : IDENT VAREQ expr")
def expr_var(p):
    var = Variable(p[0].getstr(), p[len(p) - 1])
    heap.append(var)    
    # heap.insert(random.randInt(1, 10000000), var)

@pg.production("expr : IDENT VAREQ LISTSTART expr LISTEND")
def expr_list(p): 
    lst = []

    for tkn in p[3]:
        if type(expr) == int:
            lst.append(tkn)

    ast_lst = List(p[0].getstr(), lst[0])

    for e in lst:
        ast_lst.add_elem(e)

    heap.append(ast_lst)        

    # parsed_expr = []    
    # try:
    #     parsed_expr = p[3].split(",") 
    # except:        
    #     parsed_expr.append(p[3])
    
    # lst = List(p[0].getstr(), parsed_expr[0])      

    # try:
    #     for i in range(len(parsed_expr) - 2):
    #         lst.add_elem(parsed_expr[i])
    # except:
    #     pass    

# IDENT := [ 1 ,2 ,3 ]

@pg.production("expr : expr COMMA expr")
def expr_list_element(p):  
    print(p)  
    return p

@pg.error    
def parser_error(p):
    if p is not None:
        raise AssertionError("Error: unexpected value %s at line %s" % (p.getstr(), p.getsourcepos()))
    else:
        raise AssertionError("Error: unexpected end of input.")

lexer = lg.build()
parser = pg.build()