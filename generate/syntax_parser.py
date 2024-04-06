from lexer import runLexer
import nodes

FIRSTSET = {
    "program": ["def", "int", "double", "if", "while", "print", "return", "identifier"] ,
    "fdecls": ["def", "EPSILON"] ,
    "fdeclsEnd": [";", "EPSILON"] ,
    "fdec": ["def"],
    "params": ["int", "double", "EPSILON"],
    "paramsEnd": [",", "EPSILON"],
    "fname": ["identifier"],
    "declarations": ["int", "double"],
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

# constants for reference
ID = "identifier"
INT = "int"
DOUBLE = "double"
DOUBLEE = "doubleE"

# array to store errors
final_errors = []

# getting array of lexemes from lexer
lexemes, lexError = runLexer()
# print(lexemes)

# index of current token
curr_index = 0 
# current token [token, lexeme]
current = lexemes[curr_index]
# lookahead token
lookahead = lexemes[curr_index+1]

'''
#* get the next token(s)
- update the current index, current token and lookahead token
params: -
return: -
'''
def nextToken():
    global current, curr_index, lookahead
    curr_index += 1
    current = lookahead
    if curr_index + 1 < len(lexemes):
        lookahead = lexemes[curr_index+1]
    else: 
        # return "EOF" when current token is final 
        lookahead = "EOF"
    # print("nextToken new current: {}".format(current))
    # print("nextToken new lookahead: {}".format(lookahead))

'''
#* check the FIRSTSET for grammar operations
params: nonTerm = non-terminal lexeme to check (string)
return: type of lexeme (string)
'''
def checkFIRST(nonTerm):
    try:
        firsts = FIRSTSET[nonTerm]

        if firsts:
            if ((current[0] == ID or current[0] == INT or current[0] == DOUBLE or current[0] == DOUBLEE) and current[0] in firsts):
                # print("FIRST: {}".format(current[0]))
                return current[0]
            elif (current[1] in firsts):
                # print("FIRST: {}".format(current[1]))
                return current[1]
            else:
                # print("FIRST: null")
                return ""
        else:
            # print("FIRST: null")
            return ""
    except KeyError:
        # print("KeyError")
        return ""
    except Exception as e:
        # print(e)
        return ""
    
def checkFIRSTCustom(nonTerm, customValue):
    try:
        firsts = FIRSTSET[nonTerm]

        if firsts:
            if ((customValue[0] == ID or customValue[0] == INT or customValue[0] == DOUBLE or customValue[0] == DOUBLEE) and customValue[0] in firsts):
                # print("FIRST: {}".format(customValue[0]))
                return customValue[0]
            elif (customValue[1] in firsts):
                # print("FIRST: {}".format(customValue[1]))
                return customValue[1]
            else:
                # print("FIRST: null")
                return ""
        else:
            # print("FIRST: null")
            return ""
    except KeyError:
        # print("KeyError")
        return ""
    except Exception as e:
        # print(e)
        return ""

'''
#* match and consume the token if the current token matches both type and lexeme
params: token = the token to match
return: boolean of if the current token has been matched and consumed
'''
def match(token):
    if token == current[:2]:
        # print("matched {} and {}".format(token, current))
        nextToken()
        # print("new current: {}".format(current))
        return True
    return False

'''
#* match and consume the token if the current token type matches
used for identifiers, and numbers where the actual lexeme varies and doesn't matter
params: tokenType = the type to match
return: boolean of if the current token has been matched and consumed
'''
def matchType(tokenType):
    if tokenType == current[0]:
        nextToken()
        return True
    return False

'''
#* parse through the program
params: -
return: program AST tree, error (if any errors)
'''
def parse():
    if lexError:
        # write error to error output file
        output_errors = open('files/syntax_errors.txt', 'w')
        output_errors.writelines("Lexical errors, cannot proceed with syntax analysis.")
        output_errors.close()
        # print("Lexical errors, cannot proceed with syntax analysis.")
        return None
    # print("parse: {}".format(current))
    try:
        program = nodes.Program()
        tokenType = checkFIRST("program")
        if tokenType != "":
            program.fdecls = checkFDecls()
            program.decls = checkDeclarations()
            program.stmtSeq = checkStmtSeq()
            if not match(['delim', '.']):
                final_errors.append('syntax error: expecting "." at the end of the program\n')
            # printFinals(program, final_errors)
            # write results to error output file
            output_errors = open('files/syntax_errors.txt', 'w')
            output_errors.writelines(final_errors)
            output_errors.close()
            return program, len(final_errors) > 0
        else:
            final_errors.append('syntax error (line {}): illegal lexeme ({}) for program\n'.format(current[2], current[1]))
            # printFinals(program, final_errors)
    except Exception as e:
        # print(e)
        final_errors.append('error: {}\n'.format(e))

'''
#* check function declarations
<fdecls> ::= <fdec>; | <fdecls> <fdec>; | e
<fdecls> ::= <fdeclsEnd> | <fdec>;
<fdeclsEnd> ::= <fdec>; <fdeclsEnd> | e
params: -
returns: list of fdecNodes
'''
def checkFDecls():
    nodes = []
    while current[1] != "EOF" and checkFIRST("fdecls") != "":
        node = checkFDef()
        nodes.append(node)
        if not match(['delim', ';']):
            final_errors.append('syntax error (line {}): expected ";" after function definition, recieved "{}"\n'.format(current[2], current[1]))
    return nodes

'''
#* get function declaration
params: -
return: fdef (fdefNode)
'''
def checkFDef():
    fdef = nodes.fdefNode()
    if match(['fdec', 'def']):
        fdef.line = current[2]
        if checkFIRST("type") == "":
            final_errors.append('syntax error (line {}): expected function return type after def, recieved "{}"\n'.format(current[2], current[1]))
        # match function return type
        fdef.type = current[:2]
        matchType("type")
        if current[0] != ID:
            final_errors.append('syntax error (line {}): expected function name after return, recieved "{}"\n'.format(current[2], current[1]))
        # match fname
        fdef.fname = current[:2]
        matchType(ID)
        if match(['delim', '(']) == "":
            final_errors.append('syntax error (line {}): expected "(" after function name, recieved "{}"\n'.format(current[2], current[1]))
        # get params
        fdef.params = []
        while current[1] != "EOF" and checkFIRST("params") != "":
            param = checkParam()
            fdef.params.append(param)
            matchedComma = match(['delim', ','])
            if not matchedComma and current[:2] != ['delim', ')'] and checkFIRSTCustom("params", lookahead) != "":
                print(current)
                print(lookahead)
                # no comma, no bracket, but another param lookahead
                final_errors.append('syntax error (line {}): expected comma when multiple parameters, recieved "{}"\n'.format(current[2], current[1]))
                nextToken()
            elif matchedComma and checkFIRSTCustom("params", current) == "":
                # comma, but no more params
                final_errors.append('syntax error (line {}): expected another parameter after comma, recieved "{}"\n'.format(current[2], current[1]))
        
        if not match(['delim', ')']):
            final_errors.append('syntax error (line {}): expected ")" after function parameters, recieved "{}"\n'.format(current[2], current[1]))
        
        fdef.decls = checkDeclarations()
        fdef.stmtSeq = checkStmtSeq()

        if not match(['fdec', 'fed']):
            final_errors.append('syntax error (line {}): expected fed at the end of the function definition, recieved "{}"\n'.format(current[2], current[1]))
    
    else:
        final_errors.append('syntax error (line {}): expected "def" for function definition, recieved "{}"\n'.format(current[2], current[1]))

    return fdef


'''
#* check parameter
params: -
return: param (paramNode)
'''
def checkParam():
    param = nodes.paramNode()
    if match(['type', 'int']):
        param.type = ['type', 'int']
        param.var = checkVar()
    elif match([['type', 'double']]):
        param.type = ['type', 'double']
        param.var = checkVar()
    else:
        final_errors.append('syntax error (line {}): expected a type for param, recieved "{}"\n'.format(current[2], current[1]))
    return param

'''
#* check declarations
- note: decl will end with a semicolon (<decl>;)
<declarations> ::= <decl>; | <declarations> <decl>; | e
<declarations> ::= <decl>; <declarationsEnd>
<declarationsEnd> :== <decl> ; <declarationsEnd> | ;
params: -
return: nodes = list of decls (declNodes)
'''
def checkDeclarations():
    # print("checkDeclarations: {}".format(current))
    nodes = []
    while current[1] != "EOF" and checkFIRST("declarations") != "":
        node = checkDecl()
        nodes.append(node)
        if (not match(["delim", ";"])):
            final_errors.append('syntax error (line {}): expected ";" after declaration, recieved "{}"\n'.format(current[2], current[1]))
        nodesEnd = checkDeclarationsEnd()
        nodes.extend(nodesEnd)
    if checkFIRST("fdecls"):
        final_errors.append('syntax error (line {}): function declarations should be before declarations, recieved "{}"\n'.format(current[2], current[1]))
    return nodes

'''
#* check decl
<decl> := <type> <varlist>
params: -
return: node (declNode)
'''
def checkDecl():
    # print("checkDecl: {}".format(current))
    tokenType = checkFIRST("decl")
    node = nodes.declNode()

    if tokenType != "":
        node.type = current[:2]
        node.line = current[2]
        match(current[:2])
        if not checkFIRST("varlist"):
            final_errors.append('syntax error (line {}): expected variable name after declaration, recieved "{}"\n'.format(current[2], current[1]))
        node.varlist = checkVarlist()
        return node
    else:
        final_errors.append('syntax error (line {}): expected type for declaration, recieved "{}"\n'.format(current[2], current[1]))
    return None

'''
#* check declarations end
<declarations> ::= <decl>; | <declarations> <decl>; | e
<declarations> ::= <decl>; <declarationsEnd>
<declarationsEnd> :== <decl> ; <declarationsEnd> | ;
params: -
return: nodes = array of decl (declNode)
'''
def checkDeclarationsEnd():
    # print("checkDeclarationsEnd: {}".format(current))
    tokenType = checkFIRST("declarationsEnd")
    nodes = []

    if tokenType != "":
        node = checkDecl()
        nodes.append(node)
        if not match(["delim", ";"]):
            final_errors.append('syntax error (line {}): expected ";" after declaration, recieved "{}"\n'.format(current[2], current[1]))
        nodesEnd = checkDeclarationsEnd()
        nodes.extend(nodesEnd)
    return nodes

'''
#* check var list
<varlist> ::= <var>, <varlist> | <var>
<varlist> ::= <var>, <varlistEnd>
<varlistEnd> ::= , <varlist>
params: -
return: list of vars (varNode)
'''
def checkVarlist():
    # print("checkVarlist: {}".format(current))
    tokenType = checkFIRST("varlist")
    nodes = []

    if tokenType != "":
        node = checkVar()
        nodes.append(node)
        nodesEnd = checkVarlistEnd()
        nodes.extend(nodesEnd)
    return nodes

'''
#* check var
<var> ::= <id> | <id>[<expr>]
<var> ::= <id> <varEnd>
<varEnd> ::= [<expr>] | e
params: -
return: var (varNode)
'''
def checkVar():
    # print("checkVar: {}".format(current))
    tokenType = checkFIRST("var")

    if tokenType != "":
        var = nodes.varNode(current)
        matchType(ID)
        var.varEnd = checkVarEnd()
    else:
        final_errors.append('syntax error (line {}): expected identifier for var, recieved "{}"\n'.format(current[2], current[1]))
    return var

'''
#* check var end
<var> ::= <id> | <id>[<expr>]
<var> ::= <id> <varEnd>
<varEnd> ::= [<expr>] | e
params: -
return: -
'''
def checkVarEnd():
    # print("checkVarEnd: {}".format(current))
    tokenType = checkFIRST("varEnd")
    if tokenType != "":
        match(['delim', '['])
        expr = checkExpr()
        if not match(['delim', ']']):
            final_errors.append('syntax error (line {}): expected "]" after expression, recieved "{}"\n'.format(current[2], current[1]))
    return None

'''
#* check varlist end
<varlist> ::= <var>, <varlist> | <var>
<varlist> ::= <var>, <varlistEnd>
<varlistEnd> ::= , <varlist>
params: -
return: list of vars (varNode)
'''
def checkVarlistEnd():
    # print("checkVarlistEnd: {}".format(current))
    tokenType = checkFIRST("varlistEnd")
    nodes = []

    if tokenType != "":
        if match(["delim", ","]):
            nodes = checkVarlist()
    return nodes

'''
#* check statement sequence
params: -
return: statements = list of statements
'''
def checkStmtSeq():
    # print("StmtSeq: {}".format(current))
    statements = []

    while current[1] != "EOF" and checkFIRST("statementSeq") != "":
        statement = checkStatement()
        if statement is not None:
            statements.append(statement)
        matchedSemi = match(['delim', ';'])
        statementFollowings = ['fi', 'else', 'od']
        if not matchedSemi and current[1] not in statementFollowings and checkFIRSTCustom("statementSeq", lookahead) != "":
            # no semicolon, but another statement
            final_errors.append('syntax error (line {}): expected ";" between statements, recieved "{}"\n'.format(current[2], current[1]))
            nextToken()
        elif matchedSemi and checkFIRST("statementSeq") == "":
            # semicolon, but no more statements
            final_errors.append('syntax error (line {}): expected no ";" after statement, recieved "{}"\n'.format(current[2], current[1]))
    
    if checkFIRST("fdecls"):
        final_errors.append('syntax error (line {}): function declarations should be before declarations and statements, recieved "{}"\n'.format(current[2], current[1]))
    elif checkFIRST("declarations"):
        final_errors.append('syntax error (line {}): declarations should be before statements, recieved "{}"\n'.format(current[2], current[1]))

    return statements

'''
#* check statement sequence end
params: -
return: statements = list of statements
'''
def checkStmtSeqEnd():
    # print("StmtSeqEnd: {}".format(current))
    tokenType = checkFIRST("statementSeqEnd")
    statements = []

    if tokenType != "":
        match(['delim', ';'])
        statement = checkStatement()
        if statement is not None:
            statements.append(statement)
        otherStatements = checkStmtSeqEnd()
        statements.extend(otherStatements)
    return statements

'''
#* check statement
    - check for each statement case and handle accordingly?
    - assignment, if, while, builtin (build)
    params: -
    return: statement node
'''
def checkStatement():
    # print("Statement: {}".format(current))
    tokenType = checkFIRST("statement")
    stmt = None
    # assignment statement <stmt> := <var> = <expr>
    if tokenType == ID:
        if lookahead[1] == "=":
            varNode = checkVar()
            match(['operator', '='])
            if checkFIRST("expr") == "":
                final_errors.append('syntax error (line {}): expected expression after "=", recieved "{}"\n'.format(current[2], current[1]))
            exprNode = checkExpr()
            stmt = nodes.assignStmtNode(varNode, exprNode)
        else:
            final_errors.append('syntax error (line {}): expected "=" after variable, recieved "{}"\n'.format(current[2], current[1]))
            nextToken()
    # if statement
    # <stmt> := if <bexpr> then <statement_seq> fi | 
    #       if <bexpr> then <statement_seq> else <statement_seq> fi
    elif tokenType == "if":
        match(['statement', 'if'])
        bexprNode = checkBexpr()
        if not match(['statement', 'then']):
            final_errors.append('syntax error (line {}): expected "then" after if expression, recieved "{}"\n'.format(current[2], current[1]))
        stmtSeqNode = checkStmtSeq()
        if match(['statement', 'else']):
            elseStmtSeqs = checkStmtSeq()
        else:
            elseStmtSeqs = []
        if not match(['statement', 'fi']):
            final_errors.append('syntax error (line {}): expected "fi" at end of the if statement, recieved "{}"\n'.format(current[2], current[1]))
        stmt = nodes.ifStmtNode(bexprNode, stmtSeqNode, elseStmtSeqs)
    
    # while statement while <bexpr> do <statement_seq> od
    elif tokenType == "while":
        match(['statement', 'while'])
        bexprNode = checkBexpr()
        if not match(['statement', 'do']):
            final_errors.append('syntax error (line {}): expected "do" after while expression, recieved "{}"\n'.format(current[2], current[1]))
        stmtSeqNode = checkStmtSeq()
        if not match(['statement', 'od']):
            final_errors.append('syntax error (line {}): expected "od" at the end of the while statement, recieved "{}"\n'.format(current[2], current[1]))
        stmt = nodes.whileStmtNode(bexprNode, stmtSeqNode)
    
    # built in statement print <expr> 
    elif tokenType == "print":
        tt = current[:2]
        line = current[2]
        match(['statement', 'print'])
        expr = checkExpr()
        stmt = nodes.builtStmt(tt, expr, line)

    # built in statement return <expr>
    elif tokenType == "return":
        tt = current[:2]
        line = current[2]
        match(['statement', 'return'])
        expr = checkExpr()
        stmt = nodes.builtStmt(tt, expr, line)

    else:
        final_errors.append('syntax error (line {}): invalid start of statement, recieved "{}"\n'.format(current[2], current[1]))

    return stmt

'''
#* check expr sequence
params: -
return: list of expr (exprNodes)
'''
def checkExprSeq():
    # print("ExprSeq: {}".format(current))
    tokenType = checkFIRST("exprSeq")
    nodes = []

    if tokenType != "":
        node = checkExpr()
        nodes.append(node)
        nodesEnd = checkExprSeqEnd()
        nodes.extend(nodesEnd)
    return nodes

'''
#* check expr sequence end
params: -
return: list of exprNodes
'''
def checkExprSeqEnd():
    # print("ExprSeqEnd: {}".format(current))
    tokenType = checkFIRST("exprSeqEnd")
    nodes = []

    if tokenType != "":
        if match(['delim', ',']) and not checkFIRST("exprSeq"):
            final_errors.append('syntax error (line {}): invalid follow after comma in expression sequence, recieved "{}"\n'.format(current[2], current[1]))
        exprs = checkExprSeq()
        nodes.extend(exprs)
    return nodes

'''
#* check expr
params: -
return: expr (exprNode)
'''
def checkExpr():
    # print("Expr: {}".format(current))
    tokenType = checkFIRST("expr")
    expr = nodes.exprNode()
    if tokenType != "":
        expr.line = current[2]
        expr.term = checkTerm()
        expr.exprEnd = checkExprEnd()
    return expr

'''
#* check expr end
params: -
return exprEnd (exprEndNode)
'''
def checkExprEnd():
    # print("ExprEnd: {}".format(current))
    tokenType = checkFIRST("exprEnd")
    if tokenType != "":
        exprEnd = nodes.exprEndNode()
        exprEnd.op = current[:2]
        exprEnd.line = current[2]
        match(current[:2])
        exprEnd.term = checkTerm()
        exprEnd.exprE = checkExprEnd()
        return exprEnd
    return None

'''
#* check bexpr
<bexpr> ::= <bexpr> or <bterm> | <bterm>
params: -
return: bexpr = bexprNode
'''
def checkBexpr():
    # print("Bexpr: {}".format(current))
    tokenType = checkFIRST("bexpr")
    bexpr = nodes.bexprNode()

    if tokenType != "":
        bexpr.bterm = checkBterm()
        bexpr.bexprEnd = checkBexprEnd()
    
    return bexpr

'''
#* check bexpr end
params: -
return: bexprEnd (bexprEndNode) | none
'''
def checkBexprEnd():
    # print("BexprEnd: {}".format(current))
    tokenType = checkFIRST("bexprEnd")
    if tokenType != "":
        bexprEnd = nodes.bexprEndNode()
        if not match(['bexpr', 'or']):
            final_errors.append('syntax error (line {}): expected "or", recieved "{}"\n'.format(current[2], current[1]))
        bexprEnd.bterm = checkBterm()
        bexprEnd.bexprEnd = checkBexprEnd()
        return bexprEnd
    return None

'''
#* check bterm
params: -
return: bterm (btermNode)
'''
def checkBterm():
    # print("Bterm: {}".format(current))
    tokenType = checkFIRST("bterm")
    bterm = nodes.btermNode()

    if tokenType != '':
        bterm.bfactor = checkBfactor()
        bterm.btermEnd = checkBtermEnd()
    
    return bterm

'''
#* check bterm end
params: -
return: btermEnd (btermEndNode) | none
'''
def checkBtermEnd():
    # print("BtermEnd: {}".format(current))
    tokenType = checkFIRST("btermEnd")

    if tokenType != "":
        btermEnd = nodes.btermEndNode()
        if not match(['bterm', 'and']):
            final_errors.append('syntax error (line {}): expected "and", recieved "{}"\n'.format(current[2], current[1]))
        btermEnd.bfactor = checkBfactor()
        btermEnd.btermEnd = checkBtermEnd()
        return btermEnd

    return None

'''
#* check bfactor
params: -
return: bfactor (bfactorNode)
'''
def checkBfactor():
    # print("Bfactor: {}".format(current))
    tokenType = checkFIRST("bfactor")
    bfactor = nodes.bfactorNode()

    if tokenType == "not":
        bfactor.negate = True
        match(['bfactor', 'not'])
        bfact = nodes.bfactorNode()
        bfactor.bcomp = bfact
    elif tokenType == "(":
        match(['delim', '('])
        if checkFIRST("bexpr") != "":
            bexpr = checkBexpr()
            bfactor.bexpr = bexpr
        elif checkFIRST("expr") != "":
            e1 = checkExpr()
            if current[0] == "comp":
                if lookahead[:2] == ["operator", "="]:
                    comp = ["comp", current[1]+"=", current[2]]
                    matchType("comp")
                    match(["operator", "="])
                elif current[1] == "<" and lookahead[1] == ">":
                    comp = ["comp", "<>", current[2]]
                    matchType("comp")
                    matchType("comp")
                else:
                    comp = current[:2]
                    matchType("comp")
            elif current[:2] == ["operator", "="] and lookahead[:2] == ["operator", "="]:
                comp = ["comp", "==", current[2]]
                match(["operator", "="])
                match(["operator", "="])
            else:
                final_errors.append('syntax error (line {}): expected comparator, recieved "{}"\n'.format(current[2], current[1]))
            e2 = checkExpr()
            bcomp = nodes.bcompNode(e1, comp, e2)
            bfactor.bcomp = bcomp
        else:
            final_errors.append('syntax error (line {}): error parsing for boolean expression/expression in boolean factor\n'.format(current[2], current[1]))
        if not match(['delim', ')']):
            final_errors.append('syntax error (line {}): expected ")", recieved "{}"\n'.format(current[2], current[1]))
    else:
        final_errors.append('syntax error (line {}): invalid boolean factor\n'.format(current[2], current[1]))
    return bfactor

'''
#* check term
params: -
return: term (termNode)
'''
def checkTerm():
    # print("Term: {}".format(current))
    tokenType = checkFIRST("term")
    term = nodes.termNode()
    if tokenType != "":
        term.line = current[2]
        term.factor = checkFactor()
        term.termEnd = checkTermEnd()
    return term

'''
#* check term end
params: -
return: termEnd = (termEndNode)
'''
def checkTermEnd():
    # print("TermEnd: {}".format(current))
    tokenType = checkFIRST("termEnd")
    if tokenType != "":
        termEnd = nodes.termEndNode()
        termEnd.op = current[:2]
        match(current[:2])
        termEnd.factor = checkFactor()
        return termEnd
    return None

'''
#* check factor
<factor> ::= <var> | <number> | (<expr>) | <fname>(<exprseq>)
    - check for each type (identifier, number, expression or function call)
    - identifier --> check if func name (if followed by bracket) 
        if fun name save as a function node?? idk?? make function node??
        else save as var
    - number --> save node as current node
    - expression --> match open bracket, get expr, match close bracket
    params: -
    return: factor (factorNode)
'''
def checkFactor():
    # print("Factor: {}".format(current))
    tokenType = checkFIRST("factor")
    factor = nodes.factorNode()
    if tokenType != "":
        factor.line = current[2]
        if tokenType == ID:
            if lookahead[1] == "(":
                factor.type = "funcCall"
                factor.node = checkFuncCall()
            else:
                factor.type = "var"
                factor.node = checkVar()
        elif tokenType == DOUBLE or tokenType == DOUBLEE or tokenType == INT:
            factor.type = "number"
            factor.node = current[:2]
            nextToken()
        elif tokenType == "(":
            match(['delim', '('])
            factor.type = "expr"
            factor.node = checkExpr()
            if not match(['delim', ')']):
                final_errors.append('syntax error (line {}): expected ";" after declaration, recieved "{}"\n'.format(current[2], current[1]))
    else: 
        final_errors.append('syntax error (line {}): invalid factor\n'.format(current[2]))
    return factor

'''
#* check function call
params: -
return: fcall (fCallNode)
'''
def checkFuncCall():
    # print("FuncCall: {}".format(current))
    tokenType = checkFIRST("fname")
    fcall = nodes.fCallNode()

    if tokenType != "":
        fcall.fname = current[1]
        fcall.line = current[2]
        matchType(ID)
        if not match(['delim', '(']):
            final_errors.append('syntax error (line {}): expected "(" before function call, recieved "{}"\n'.format(current[2], current[1]))
        fcall.exprSeq = checkExprSeq()
        if not match(['delim', ')']):
            final_errors.append('syntax error (line {}): expected ")" before function call, recieved "{}"\n'.format(current[2], current[1]))
    return fcall

'''
#* print results from program and final_errors array
params: 
- program = program AST
- final_errors = array of errors
return: -
'''
def printFinals(program, final_errors):
    print('Final Program')
    print(program)
    print('~'*10)
    print('Final Errors')
    for error in final_errors:
        print(error.strip())

#* MAIN
# parse()