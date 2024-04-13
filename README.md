# CP471-compilers

This is my work for CP471 in Winter 2024.
For each project section, there is a `.md` file with more information. 

### How to Run Full Compiler
1. The full compiler can be run from the `generate` folder
2. Enter the name of the file with code to read on line 13 of `generate/lexer.py`
3. Run `code_gen.py`
4. The final 3TAC code is saved in `intermediate_code.txt` as a file, as well as printed.

### Files
`lex_errors.txt`: lexical analysis errors  
`syntax_errors.txt`: syntax analysis errors  
`sem_errors.txt`: semantic analysis errors  
`intermediate_code.txt`: final 3TAC intermediate code  

Errors from each analysis phase are saved in the respective txt files. The phase in which the error occurred is specified in following error files, and is printed as well.
