class ASTObject(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value        

    def evaluate(self):
        return;        
    
class Variable(ASTObject):
    def __init__(self, name, value):
        super().__init__(name, value)        

    def evaluate(self):
        return self.value

class List(ASTObject):
    def __init__(self, name, value):
        self.value = [value]
        super().__init__(name, self.value)        

    def add_elem(self, elem):
        self.value.append(elem)

    def evaluate(self):
        return list(self.value)
    
class Function(ASTObject):
    # Args :: [Variable]
    def __init__(self, name, value, args):
        super().__init__(name, value)
        self.args = args        

    def generate_pattern(self):
        ret = self.name

        # how will this work for functions with multiple arguments? DECISIONS!!
        for a in self.args:
            ret += "("
            if (not (type(a.value) == type(None))):
                ret += a.name
                ret += " :: "
                ret += str(type(a.value))
            ret += ") outs "
            ret += self.value

        return ret

    def evaluate(self):
        return self.value

class Put(Function):
    def __init__(self, args):        
        name = "put"
        value = "IO"
        super().__init__(name, value, args)        

    def get_pattern(self):
        return super().generate_pattern()

    def evaluate(self):        
        for a in self.args:
            print(str(a.value))     

class Dump(Function):
    def __init__(self, heap):        
        name = "dump"
        value = "IO"
        args = [Variable("", None)]
        self.heap = heap
        super().__init__(name, value, args)        

    def get_pattern(self):
        return super().generate_pattern()

    def evaluate(self):        
        self.heap.clear()        
        # for a in self.args:
            # print(str(a.value))     

class Poke(Function):
    def __init__(self, args, heap):
        name = "poke"
        value = "IO"
        self.heap = heap
        super().__init__(name, value, args)        
        
    def get_pattern(self):
        return super().generate_pattern()

    def evaluate(self):        
        for item in self.heap:                          
            if (str(hex(id(item))) == str(self.args[0].value)):
                print(item.name + ", " + str(item.value))
                break

class Pop(Function):
    def __init__(self, args, heap):
        name = "pop"
        value = "IO"
        self.heap = heap
        super().__init__(name, value, args)        
        
    def get_pattern(self):
        return super().generate_pattern()

    def evaluate(self):  
        index = 0      
        for item in self.heap:                          
            if (str(hex(id(item))) == str(self.args[0].value)):
                self.heap.pop(index)
                break
            index += 1

class Peak(Function):
    def __init__(self, heap):        
        name = "peak"
        value = "IO"
        args = [Variable("", None)]
        self.heap = heap
        super().__init__(name, value, args)        

    def get_pattern(self):
        return super().generate_pattern()

    def evaluate(self):        
        print(self.heap)
        # for a in self.args:
            # print(str(a.value))                 

class For(Function):  
    def __init__(self, name, value, lst):
        super(name, value)
        self.lst = lst
    
    # The value of this function should be a Function
    # This function will be applied and evaluated for each element in a given list
    def evaluate(self):
        for elem in lst:
            value.value = elem
            value.evaluate()