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
lexemes = runLexer()
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
    try:
        if curr_index + 1 < len(lexemes):
            lookahead = lexemes[curr_index+1]
        else: 
            # return "EOF" when current token is final 
            lookahead = "EOF"
        print("nextToken new current: {}".format(current))
        print("nextToken new lookahead: {}".format(lookahead))
    except:
        final_errors.append('error parsing at line {}'.format(lexemes[curr_index+1][2]))

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
                print("FIRST: {}".format(current[0]))
                return current[0]
            elif (current[1] in firsts):
                print("FIRST: {}".format(current[1]))
                return current[1]
            else:
                print("FIRST: null")
                return ""
        else:
            print("FIRST: null")
            return ""
    #TODO: add error handling!!
    except KeyError:
        # "program" is not in the dict
        print("KeyError")
        return ""
    except Exception as e:
        print(e)
        return ""
    
def checkFIRSTCustom(nonTerm, customValue):
    try:
        firsts = FIRSTSET[nonTerm]

        if firsts:
            if (customValue in firsts):
                print("FIRST: {}".format(customValue))
                return customValue
            else:
                print("FIRST: null")
                return ""
        else:
            print("FIRST: null")
            return ""
    #TODO: add error handling!!
    except KeyError:
        # "program" is not in the dict
        print("KeyError")
        return ""
    except Exception as e:
        print(e)
        return ""

'''
#* match and consume the token if the current token matches both type and lexeme
params: token = the token to match
return: boolean of if the current token has been matched and consumed
'''
def match(token):
    if token == current[:2]:
        print("matched {} and {}".format(token, current))
        nextToken()
        print("new current: {}".format(current))
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
return: -
'''
def parse():
    print("parse: {}".format(current))
    try:
        program = nodes.Program()
        tokenType = checkFIRST("program")
        if tokenType != "":
            program.fdecls = checkFDecls()
            program.decls = checkDeclarations()
            program.stmtSeq = checkStmtSeq()
            match(['delim', '.'])
            print(program)
            return program
        else:
            #TODO: log error
            print("empty tokenType == error")
    #TODO: add error handling
    except KeyError:
        # "program" is not in the dict
        print("KeyError")
    except Exception as e:
        print(e)

#! TODO: fdecl nodes and parser functions!
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
            # TODO: log error
            print("error line 204")
    return nodes

#! add in errors (wherever match functions are??) see printing errors too!!
'''
#* get function declaration
params: -
return: fdef (fdefNode)
'''
def checkFDef():
    fdef = nodes.fdefNode()
    #TODO add errors here
    if match(['fdec', 'def']):
        if checkFIRST("type") == "":
            print("error fdef type line 217")
        # match function return type
        fdef.type = current[:2]
        matchType("type")
        if current[0] != ID:
            print("error fdef id")
        # match fname
        fdef.fname = current[:2]
        matchType(ID)
        if match(['delim', '(']) == "":
            print("error fdef (")
        # get params
        fdef.params = []
        while current[1] != "EOF" and checkFIRST("params") != "":
            param = checkParam()
            fdef.params.append(param)
            matchedComma = match(['delim', ','])
            if not matchedComma and checkFIRSTCustom("params", lookahead[1]) != "":
            # no comma, but another param
                print("error line 397")
                nextToken()
            elif matchedComma and checkFIRSTCustom("params", current[1]) == "":
                # comma, but no more params
                print("error line 399")
        
        if not match(['delim', ')']):
            print("error fdef )")
        
        fdef.decls = checkDeclarations()
        fdef.stmtSeq = checkStmtSeq()

        if not match(['fdec', 'fed']):
            print("error fdef fed")
    
    else:
        print("error fdec def")

    return fdef


'''
#* check parameter
params: -
return: param (paramNode)
'''
def checkParam():
    param = nodes.paramNode(current[:2])
    matchType('type')
    param.var = checkVar()
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
    print("checkDeclarations: {}".format(current))
    nodes = []
    while current[1] != "EOF" and checkFIRST("declarations") != "":
        node = checkDecl()
        nodes.append(node)
        #TODO: handle if match returns false
        if (not match(["delim", ";"])):
            print("error line 260")
        nodesEnd = checkDeclarationsEnd()
        nodes.extend(nodesEnd)
    #TODO: handle errors? (and do so for the rest?)
    return nodes

'''
#* check decl
<decl> := <type> <varlist>
params: -
return: node (declNode)
'''
def checkDecl():
    print("checkDecl: {}".format(current))
    tokenType = checkFIRST("decl")
    node = nodes.declNode()

    if tokenType != "":
        node.declNode = current[:2]
        match(current[:2])
        #TODO double check this is actually a valid thing to do
        node.varlist = checkVarlist()
        return node
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
    print("checkDeclarationsEnd: {}".format(current))
    tokenType = checkFIRST("declarationsEnd")
    nodes = []

    if tokenType != "":
        node = checkDecl()
        nodes.append(node)
        #TODO: handle if match returns false
        match(["delim", ";"])
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
    print("checkVarlist: {}".format(current))
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
    print("checkVar: {}".format(current))
    tokenType = checkFIRST("var")

    if tokenType != "":
        var = nodes.varNode(current)
        matchType(ID)
        var.varEnd = checkVarEnd()
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
    print("checkVarEnd: {}".format(current))
    #TODO: double check
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
    print("checkVarlistEnd: {}".format(current))
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
    print("StmtSeq: {}".format(current))
    statements = []

    while current[1] != "EOF" and checkFIRST("statementSeq") != "":
        statement = checkStatement()
        if statement is not None:
            statements.append(statement)
        # otherStatements = checkStmtSeqEnd()
        # statements.extend(otherStatements)
        matchedSemi = match(['delim', ';'])
        if not matchedSemi and checkFIRSTCustom("statementSeq", lookahead[1]) != "":
            # no semicolon, but another statement
            print("error line 397")
            nextToken()
        elif matchedSemi and checkFIRSTCustom("statementSeq", current[1]) == "":
            # semicolon, but no more statements
            print("error line 399")
    return statements

'''
#* check statement sequence end
params: -
return: statements = list of statements
'''
def checkStmtSeqEnd():
    print("StmtSeqEnd: {}".format(current))
    tokenType = checkFIRST("statementSeqEnd")
    statements = []

    if tokenType != "":
        if not match(['delim', ';']):
            print("error line 409")
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
    #TODO: try logging errors into array here?? like in lexer?
'''
def checkStatement():
    print("Statement: {}".format(current))
    tokenType = checkFIRST("statement")
    stmt = None
    # assignment statement <stmt> := <var> = <expr>
    if tokenType == ID:
        if lookahead[1] == "=":
            varNode = checkVar()
            match(['operator', '='])
            exprNode = checkExpr()
            stmt = nodes.assignStmtNode(varNode, exprNode)
        else:
            print("error checkStatement line 469")
            #TODO: log error
    # if statement
    # <stmt> := if <bexpr> then <statement_seq> fi | 
    #       if <bexpr> then <statement_seq> else <statement_seq> fi
    elif tokenType == "if":
        match(['statement', 'if'])
        bexprNode = checkBexpr()
        match(['statement', 'then'])
        stmtSeqNode = checkStmtSeq()
        if match(['statement', 'else']):
            elseStmtSeqs = checkStmtSeq()
        else:
            elseStmtSeqs = []
        match(['statement', 'fi'])
        stmt = nodes.ifStmtNode(bexprNode, stmtSeqNode, elseStmtSeqs)
    
    # while statement while <bexpr> do <statement_seq> od
    elif tokenType == "while":
        match(['statement', 'while'])
        bexprNode = checkBexpr()
        match(['statement', 'do'])
        stmtSeqNode = checkStmtSeq()
        match(['statement', 'od'])
        stmt = nodes.whileStmtNode(bexprNode, stmtSeqNode)
    
    # built in statement print <expr> 
    elif tokenType == "print":
        tt = current[:2]
        match(['statement', 'print'])
        expr = checkExpr()
        stmt = nodes.builtStmt(tt, expr)

    # built in statement return <expr>
    elif tokenType == "return":
        tt = current[:2]
        match(['statement', 'return'])
        expr = checkExpr()
        stmt = nodes.builtStmt(tt, expr)

    return stmt

'''
#* check expr sequence
params: -
return: list of expr (exprNodes)
'''
def checkExprSeq():
    print("ExprSeq: {}".format(current))
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
    print("ExprSeqEnd: {}".format(current))
    tokenType = checkFIRST("exprSeqEnd")
    nodes = []

    if tokenType != "":
        match(['delim', ','])
        exprs = checkExprSeq()
        nodes.extend(exprs)
    return nodes

'''
#* check expr
params: -
return: expr (exprNode)
'''
def checkExpr():
    print("Expr: {}".format(current))
    tokenType = checkFIRST("expr")
    expr = nodes.exprNode()
    if tokenType != "":
        expr.term = checkTerm()
        expr.exprEnd = checkExprEnd()
    return expr

'''
#* check expr end
params: -
return exprEnd (exprEndNode)
'''
def checkExprEnd():
    print("ExprEnd: {}".format(current))
    tokenType = checkFIRST("exprEnd")
    if tokenType != "":
        exprEnd = nodes.exprEndNode()
        exprEnd.op = current[:2]
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
    print("Bexpr: {}".format(current))
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
    print("BexprEnd: {}".format(current))
    tokenType = checkFIRST("bexprEnd")
    if tokenType != "":
        bexprEnd = nodes.bexprEndNode()
        match(['bexpr', 'or'])
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
    print("Bterm: {}".format(current))
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
    print("BtermEnd: {}".format(current))
    tokenType = checkFIRST("btermEnd")

    if tokenType != "":
        btermEnd = nodes.btermEndNode()
        match(['bterm', 'and'])
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
    print("Bfactor: {}".format(current))
    tokenType = checkFIRST("bfactor")
    print(tokenType)
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
                # TODO: throw error here!
                print("error bfactor line 368")
            #TODO fix error with reading comp when it's the last character in lexer!!
            e2 = checkExpr()
            bcomp = nodes.bcompNode(e1, comp, e2)
            bfactor.bcomp = bcomp
        else:
            #TODO log error here
            print("error here bfactor 2.3")
        match(['delim', ')'])
    else:
        #TODO log error here
        print("eror here bfactor 3.3")
    return bfactor

'''
#* check term
params: -
return: term (termNode)
'''
def checkTerm():
    print("Term: {}".format(current))
    tokenType = checkFIRST("term")
    term = nodes.termNode()
    if tokenType != "":
        term.factor = checkFactor()
        term.termEnd = checkTermEnd()
    return term

'''
#* check term end
params: -
return: termEnd = (termEndNode)
'''
def checkTermEnd():
    print("TermEnd: {}".format(current))
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
    print("Factor: {}".format(current))
    tokenType = checkFIRST("factor")
    factor = nodes.factorNode()
    if tokenType != "":
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
                print("error line 717")
                #TODO: add error saving
    return factor

'''
#* check function call
params: -
return: fcall (fCallNode)
'''
def checkFuncCall():
    print("FuncCall: {}".format(current))
    tokenType = checkFIRST("fname")
    fcall = nodes.fCallNode()

    if tokenType != "":
        fcall.fname = current[1]
        matchType(ID)
        match(['delim', '('])
        fcall.exprSeq = checkExprSeq()
        match(['delim', ')'])
    return fcall

#* MAIN
# print("("=="not")
parse()