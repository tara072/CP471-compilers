# Syntax Analysis
*Documentation for the syntax analysis section of my project*

### How to Run
1. Enter the name of the file with code to read on line 13 of `lexer.py`
2. Run `parser.py`
3. The program will run and print out updates as a log of it's current run
4. At the end, it will print the AST of the results and the errors

### First and Follow Table
The First values are also in the code in `parser.py`
| non-terminal | FIRST | FOLLOW |
|---|---|---|
| program | def | $ |
| fdecls | def | int, double |
| fdeclsEnd | def | int, double |
| fdec | def | ; |
| params | int, double | ) |
| declarations | int, double | {any letter}, if,<br>while, print, return |
| declarationsEnd | int, double | {any letter}, if,<br>while, print, return |
| decl | int, double | ; |
| type | int, double | {any letter} |
| varlist | {any letter} | ; |
| varlistEnd | , | ; |
| var | {any letter} | ., ), ,, *, /, %, +,<br>-, ], ;, =, <, >, ==,<br><=, >=, <>, fi, else,<br>od, fed |
| statementSeq | {any letter}, if<br>while, print, return | ., fi, else, od, fed |
| statement | {any letter}, if,<br>while, print, return | ., ;, fi, else,<br>od, fed |
| expr | {any letter},<br>{any number}, ( | ., ), ,, ], ;, <, >, ==,<br><=, >=, <>, fi, else,<br>od, fed |
| exprEnd | +, - | ., ), ,, ], ;, <, >, ==,<br><=, >=, <>, fi, else,<br>od, fed |
| term | {any letter}, <br>{any number}, ( | ., ), ,, ], ;, <, >, ==,<br><=, >=, <>, fi, else,<br>od, fed |
| termEnd | *, /, % | ., ), ,, +, -, ], ;, <, >, ==,<br><=, >=, <>, fi, else,<br>od, fed |
| factor | {any letter},<br>{any number}, ( | ., ), ,, *, /, %, +,<br>-, ], ;, =, <, >, ==,<br><=, >=, <>, fi, else,<br>od, fed |
| exprSeq | {any letter}, <br>{any number}, ( | ) |
| bexpr | (, not | ), then, do |
| bexprEnd | or | ), then, do |
| bterm | (, not | ), or, then, do |
| btermEnd | and | ), or, then, do |
| bfactor | (, not | ), and, or, then, do |
| bfactorEnd |  | ) |
| comp | <, >, ==, <=, >=, <> | {any letter}, {any number}, ( |
| digit | {any number} | {any letter}, {any number},<br>(, [, ., ), ,, *, /, %, +,<br>-, ], ;, =, <, >, ==,<br><=, >=, <>, fi, else,<br>od, fed |
| integer | {any number} | ., ), ,, *, /, %, +,<br>-, ], ;, <, >, ==,<br><=, >=, <>, fi, else,<br>od, fed |
| integerEnd | {any number} | ., ), ,, *, /, %, +,<br>-, ], ;, <, >, ==,<br><=, >=, <>, fi, else,<br>od, fed |
| double | {any number} | ., ), ,, *, /, %, +,<br>-, ], ;, <, >, ==,<br><=, >=, <>, fi, else,<br>od, fed |
| doubleEnd | {any number} | ., ), ,, *, /, %, +,<br>-, ], ;, <, >, ==,<br><=, >=, <>, fi, else,<br>od, fed |
| number | {any number} | ., ), ,, *, /, %, +,<br>-, ], ;, <, >, ==,<br><=, >=, <>, fi, else,<br>od, fed |
| letter | {any letter} | {any letter}, {any number},<br>(, [, ., ), ,, *, /, %, +,<br>-, ], ;, <, >, =, ==,<br><=, >=, <>, fi, else,<br>od, fed |
| id | {any letter} | (, [, ., ), ,, *, /, %, +,<br>-, ], ;, <, >, =, ==,<br><=, >=, <>, fi, else,<br>od, fed |
| idEnd | {any letter},<br>{any number} | (, [, ., ), ,, *, /, %, +,<br>-, ], ;, <, >, =, ==,<br><=, >=, <>, fi, else,<br>od, fed |
| fname | {any letter} | (, [, ., ), ,, *, /, %, +,<br>-, ], ;, <, >, =, ==,<br><=, >=, <>, fi, else,<br>od, fed |

### Errors
 There is one output file: `errors.txt` to store any syntax errors that occur within the project.
