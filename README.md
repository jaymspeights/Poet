# Poet
An interpreted programming language and it's interpreter in Python

In poet, the characters you use don't matter. All that matters is the length of words, where a word is any string of symbols excluding any whitespace characters. For example, the program to print the numbers
1 - 100 looks like:


## Syntax
Program     -> [...Statement]
Statement   -> Operation | Control | Syscall
Operation   -> operator + Expression + [,Expression]
Expression  -> Operation | number | variable
Control     -> {if|while} + Expression + Block + eob
Block       -> block_marker + [...Statement] + block_marker
Syscall     -> call + [,Expression]

Each symbol in Poet is made up of a few words. The table below shows the length of each word required to form a specific symbol. Any reference to a number means that a word of that length is needed to construct the symbol. i.e. 4 2 would require a word of length four and of length two, separated by whitespace:
```
1234 12
four     to
____ __
```
The three lines above all represent the symbol made up of 4 2

### Operations
4 2 -> Assign -> (:Operator) (variable identifier: Expression) (value: Expression)
4 3 -> Add -> (:Operator) (term1: Expression) (term2: Expression)
4 4 -> Subtract -> (:Operator) (term1: Expression) (term2: Expression)
4 5 -> Multiply -> (:Operator) (term1: Expression) (term2: Expression)
4 6 -> Divide -> (:Operator) (term1: Expression) (term2: Expression)
4 7 -> Mod -> (:Operator) (term1: Expression) (term2: Expression)

*The following operations are comparisons. Conditionals in Poet check for Expression > 0. The comparison operations can be used outside of conditionals and will return 0 for true and 1 for false*
6 2 -> Not -> (:Operator) (term: Expression)
6 3 -> Equal -> (:Operator) (term1: Expression) (term2: Expression)
6 4 -> Less Than -> (:Operator) (term1: Expression) (term2: Expression)
6 5 -> Less Than or Equal-> (:Operator) (term1: Expression) (term2: Expression)

### Flow Control
2 4 -> If Statement -> (if :Control) (condition :Expression) (code :Block)
2 5 -> While Loop -> (while :Control) (condition :Expression) (code :Block)

#### Block
2 3 -> block_marker -> (:block_marker) [...code: Statement] (:block_marker)

### Numbers
*The second number represents the amount of digits minus one and the following numbers represent the values of the digits modulus ten. For example, 3 4 2 1 10 represents the number 210. 3 means number, 4 means (4-1) 3 digits, and then the following 2, 1, and 0 are used to construct the number 210. We can construct the number 0 with the symbol 3 1*
3 # ...# -> number -> (number: 3) (digits: #-1) [...value: #%10]

### Variables
*Accessing variables can be done in two ways. The first way is the most common, and is done using the symbol 1 # where # is the identifier of the variable. The second way is using the Get_Addr Syscall, which returns the value of the variable with the given identifier*
5 # -> variable -> (variable: 5) (identifier: #)

### Syscalls
*Gets the variable whos identifier is equal to the value returned by the expression*
7 2 -> get_addr (syscall: 2) (addr: Expression)
*Prints the following expression*
7 5 -> print -> (syscall: 5) (to_print: Expression)
