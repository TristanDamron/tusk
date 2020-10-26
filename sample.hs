-*
Tusk : Design Document (.tusk)
a functional, readable, interpreted language with the best of imperative languages
*-

DATA TYPES:
     Any
     Int
     Integer
     Float
     Double
     Char
     Boolean
     []
     ()
     IO
     Procedure
     None (hidden data type, not valid for variable declarations)
     
BUILT IN FUNCTIONS:
      put gets [Char] outs IO
      main outs IO
      getLine outs [Char]
      for gets (Any) [Any] outs Any
      peak gets () outs IO
      dump gets () outs IO

OPERATORS:
      Eq (==)
      Add (+)
      Subtract (-)
      Divide (/)
      Multiplication (*)
      Ord (<, >, <=, >=)
      Append (+=)
      Delete (-=)

GRAMMAR:
      -- PATTERN : <identifier> <gets, outs> <type,..> <outs> <type>
      CUSTOMFUNCTION : <identifier> (<identifier> :: <type>).. = <statement> ;
      EXPRESSION (FUNCTION) : <identifier> (<identifier>) ;
      EXPRESSION (VARIABLE) : <identifier> := <type> ;
      EXPRESSION (PROCEDURE) : <identifier> (<identifier> :: <type>).. = { <statement> } ;
      EXPRESSION (ADD) : <expression> + <expression>
      EXPRESSION (SUBTRACT) : <expression> - <expression>
      EXPRESSION (DIVIDE) : <expression> / <expression>
      EXPRESSION (MULTIPLY) : <expression> * <expression>
      EXPRESSION (EQ) : <expression> == <expression>
      EXPRESSION (OR) : <expression> <,>,<=,>= <expression>
      STATEMENT: <expression> ;


























-- sayHello outs IO
sayHello = put("Hello world!");

-- add gets Int Int outs Int
add (x :: Int) (y :: Int) = x + y;

-- fib gets Int outs Int
fib (x :: 0) = x;
fib (x :: Int) = fib(x - 1) + fib(x - 2);

-*
Multiline comment
*-

-- {} can be used as a monad to group a procedure. Must out Procedure

-- main outs Procedure
main = {
     put(add(2, 2));
     sayHello;

     -- Declaring a variable with :=
     x := 1;

     -- if statements can be used in a procedure but MUST include coverage for *all* cases. 
     if ((x > 0) then
     	put("Positive"));

     if ((x < 0) then
     	put("Negative"));

     if ((x == 0) then
     	put("x is 0!"));

     name := getLine;

     sayMyName name;

     -- Enumerations!
     nums := [1..5]
     allItems nums;

     repeat(put("Hello!")), 3);
     -- Hello! Hello! Hello!

     -- Recursive procedures
     main;
}

-- sayMyName gets [Char] outs Procedure
sayMyName (n :: [Char]) = {
     put n;
     put "Nice to meet you " += n;
}

--allItems gets [Int] outs Procedure
allItems (x :: [Int]) = for ((lambda i -> put i), x);
     -- Anonymous functions can return Any
