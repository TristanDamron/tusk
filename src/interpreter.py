from parse import *
import sys
import os

input_stream = ""

def main():            
    print("TUSKi :: v0.0.2")
    input_stream = input(">>> ")
    while not (input_stream == ":q"):         
        if not commands(input_stream):                        
            if "--" in input_stream:
                pass
            else:
                if not (input_stream is ""):                                   
                    parser.parse(lexer.lex(input_stream))                
                for i in get_stack():                    
                    i.evaluate()

                get_stack().clear()                    

        input_stream = input(">>> ")

def function_info(function_name):
    if function_name == "put":
        print(Put([Variable("x", "")]).get_pattern())
        print(Put([Variable("x", 1)]).get_pattern())
        print(Put([Variable("x", 0.2)]).get_pattern())
        print(Put([Variable("x", True)]).get_pattern())
    elif function_name == "dump":
        print(Dump([]).get_pattern())
    elif function_name == "peak":
        print(Peak([]).get_pattern())   
    elif function_name == "pop":
        print(Pop([Variable("x", "")],[]).generate_pattern())
    elif function_name == "poke":
        print(Poke([Variable("x", "")],[]).generate_pattern())
    else:
        print("Error: No definition for " + str(function_name))

def load_module(file_name):                
    try:
        raw = ""
        f = open(file_name, "r")
        line = f.readline()
        while line:
            if not ("--" in line):
                raw += line
            line = f.readline()                
    except:
        print("Error:" + file_name + " not found.")
            
    rawtkns = []
    for line in raw.split(";"):
        if line is not "\n" and line is not "":
            rawtkns.append(line + ";")
                    
    for rawtkn in rawtkns:
        if rawtkn is not '':
            parser.parse(lexer.lex(rawtkn))    

    for i in get_stack():                            
        i.evaluate()

    get_stack().clear()
        

def commands(input_string):
    input_string = input_string.lower()
    if ":" in input_string:
        if input_string == ":c":
            os.system("clear")
            return True
        elif input_string == ":h":
            # Display help text file in the terminal window
            try:
                help_text = open("help", "r")
                print(help_text.read())
            except:
                print("Error: Help file not found.")
            
            return True
        elif ":l" in input_string:
            load_module(input_string.split(" ")[1])
            return True
        elif ":i" in input_string:
            function_info(input_string.split(" ")[1])
            return True
        else:
            return False
    else:
        return False

if __name__ == "__main__":
    main()