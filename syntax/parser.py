from lexer import runLexer

FIRSTSET = {
    "program": ["def", "int", "double", "if", "while", "print", "return", "identifier"] ,
    "fdecls": ["def", "EPSILON"] ,
    "fdeclsEnd": ["def", "EPSILON"] ,
    "fdec": ["def"],
    "fdecEnd": ["def", "EPSILON"],
    "params": ["int", "double", "EPSILON"],
    "paramsEnd": [",", "EPSILON"],
    "fname": ["identifier"],
    "declarations": ["int", "double", "EPSILON"],
    "declarationsEnd": ["int", "double", "EPSILON"],
    "decl": ["int", "double"],
    "declEnd": ["int", "double", "EPSILON"],
    "type": ["int", "double"],
    "varlist": ["identifier"],
    "varlistEnd": [",", "EPSILON"],
    "statementSeq": ["if", "while", "print", "return", "identifier", "EPSILON"],
    "statementSeqEnd": [";", "EPSILON"],
    "statement": ["if", "while", "print", "return", "identifier", "EPSILON"],
    "else": ["else", "EPSILON"],
    "expr": ["identifier", "double", "int", "doubleE", "("],
    "exprEnd": ["+", "-", "EPSILON"],
    "term": ["identifier", "double", "int", "doubleE", "("],
    "termEnd": ["*", "/", "%", "EPSILON"],
    "factor": ["identifier", "int", "double", "doubleE", "("],
    "exprSeq": ["identifier", "double", "int", "doubleE", "("],
    "exprSeqEnd": [",", "EPSILON"],
    "bexpr": ["not", "("],
    "bexprEnd": ["or", "EPSILON"],
    "bterm": ["not", "("],
    "btermEnd": ["and", "EPSILON"],
    "bfactor": ["not", "("],
    "bfactorEnd": ["EPSILON"],
    "comp": ["<", ">", "==", "<=", ">=", "<>"],
    "var": ["identifier"],
    "varEnd": ["[", "EPSILON"],
}

# getting array of lexemes from lexer
# lexemes = runLexer()
lexemes = [
    "<statement, print>",
    "<int, 21>",
    "<identifier, gcd>",
    "<delim, (>",
    "<int, 21>",
    "<delim, ,>",
    "<int, 15>",
    "<delim, )>",
    "<delim, .>"
    ]

# index of current token
current = 0 
# current token [token, lexeme]
curr_token = lexemes[current][1:-1].split(',')
# lookahead token
lookahead = lexemes[current+1][1:-1].split(',')

'''
#* get the next token(s)
- update the current index, current token and lookahead token
params: -
return: -
'''
def nextToken():
    global curr_token, current, lookahead
    current += 1
    curr_token = lookahead
    lookahead = lexemes[current+1][1:-1].split(',')

# print(curr_token)
# print(lookahead)
# nextToken()
# print(curr_token)
# print(lookahead)

'''
#* check the FIRSTSET for grammar operations
params: lex = non-terminal lexeme to check (string)
return: first = type of lexeme (string)
'''
def checkFIRST(lex):
    print(FIRSTSET[lex])

checkFIRST('program')