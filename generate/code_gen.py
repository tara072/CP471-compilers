from analyser import analyse
import nodes

rootTable, program, semErr = analyse()
code = [] #3TAC generated code

# counts for tracking
tempCount = 1
boolLabelCount = 1
orLabelCount = 1
andLabelCount = 1
ifCount = 1
localTempCount = 1
    
# map of operators to compare
compOps = {
    '>': 'BGT',
    '<': 'BLT',
    '>=': 'BGE',
    '<=': 'BLE',
    '<>': 'BNE',
    '==': 'BEQ'
}

def generate():
    if semErr:
        # write error to error output file
        if isinstance(semErr, str):
            print(semErr)
            outputFile(semErr)
            return None, semErr
        else:
            outputFile("Semantic errors, cannot proceed with intermediate code generation.")
            print("Semantic errors, cannot proceed with intermediate code generation.")
        return None, "Semantic errors, cannot proceed with intermediate code generation."

    code.append("B main")

    # functions
    global localTempCount
    for func in program.fdecls:
        funcTable = rootTable.functions[func.fname[1]]
        localTempCount = 0

        code.append(func.fname[1] + ":")
        code.append("push LR")
        funcBeginIndex = len(code)
        code.append("begin temp")

        # go through params
        paramPoint = 4
        for param in func.params:
            paramPoint += 4
            code.append("{} = [sp + {}]".format(param.var.id[1], paramPoint))
        genStmts(func.stmtSeq)
        
        memorySize = (len(funcTable.table.variables) * 4) + localTempCount*4
        code[funcBeginIndex] = "begin {}".format(memorySize)
        code.append("pop {PC}")
    
    code.append("main:")
    mainBeginIndex = len(code)
    code.append("begin temp main")
    localTempCount = 0

    # generate statements
    genStmts(program.stmtSeq)
    memorySize = (len(rootTable.variables) * 4) + localTempCount*4
    code[mainBeginIndex] = "begin {}".format(memorySize)

    # wrap up
    printFinal(code)
    outputFile(code)
    return code
'''
#* generate statements
params:
- stmtSeq (stmtSeq arrays)
return: -
'''
def genStmts(stmtSeq):
    for stmt in stmtSeq:
        if isinstance(stmt, nodes.assignStmtNode):
            first = stmt.var.id[1]
            second = genExpr(stmt.expr)
            code.append("{} = {}".format(first, second))
        elif isinstance(stmt, nodes.ifStmtNode):
            genBExpr(stmt.bexpr, "", "", False)
            ifLabel, elseLabel, endIfLabel = getPrevIfLabel()
            code.append("{}:".format(ifLabel))
            genStmts(stmt.stmtSeq)
            code.append("b {}".format(endIfLabel))
            code.append("{}:".format(elseLabel))
            if len(stmt.elseStmtSeq) > 0:
                genStmts(stmt.elseStmtSeq)
            code.append("{}:".format(endIfLabel))
        elif isinstance(stmt, nodes.whileStmtNode):
            genBExpr(stmt.bexpr, "", "", False)
            ifLabel, elseLabel, endIfLabel = getPrevIfLabel()
            code.append("{}:".format(ifLabel))
            genStmts(stmt.stmtSeq)
            boolLabel = getPrevBoolLabel()
            code.append("b {}".format(boolLabel))
            code.append("{}:".format(elseLabel))
            code.append("{}:".format(endIfLabel))
        elif isinstance(stmt, nodes.builtStmt):
            if stmt.type[1] == "return":
                second = genExpr(stmt.expr)
                code.append("r1 = {}".format(second))
            elif stmt.type[1] == "print":
                second = genExpr(stmt.expr)
                code.append("print {}".format(second))
'''
#* generate expr
params:
- expr (exprNode)
return: 
- first (string): term
'''
def genExpr(expr):
    first = genTerm(expr.term)
    if expr.exprEnd is not None:
        termQ, opQ = genExprEnd(expr.exprEnd, [], [])
        for i in range(len(termQ)):
            temp = newTempVar()
            op = opQ[i]
            second = termQ[i]
            code.append("{} = {} {} {}".format(temp, first, op, second))
    return first

'''
#* generate exprEnd
params:
- expr (exprEndNode)
- termQ (queue): track terms in order
- opQ (queue): track ops in order
return:
- termQ (queue): track terms in order
- opQ (queue): track ops in order
'''
def genExprEnd(expr, termQ, opQ):
    term = genTerm(expr.term)
    termQ.append(term)
    opQ.append(expr.op[1])
    if expr.exprE is not None:
        return genExprEnd(expr.exprEnd, termQ, opQ)
    return termQ, opQ

'''
#* generate term
params:
- term (termnode)
return:
- term (string)
'''
def genTerm(term):
    first = genFactor(term.factor)
    if term.termEnd is not None:
        temp = newTempVar()
        op = term.termEnd.op[1]
        second = genFactor(term.termEnd.factor)
        code.append("{} = {} {} {}".format(temp, first, op, second))
        return temp
    return first

'''
#* generate factor
params:
- factor (factorNode)
return:
- term (string)
'''
def genFactor(factor):
    if factor.type == "number":
        temp = newTempVar()
        code.append("{} = {}".format(temp, factor.node[1]))
        return(temp)
    elif factor.type == "expr":
        return genExpr(factor.node)
    elif factor.type == "funcCall":
        fCallNode = factor.node
        args = []
        for expr in fCallNode.exprSeq:
            temp = genExpr(expr)
            args.append(temp)
        # for arg in args:
        for i in range(len(args) - 1, -1, -1):
            code.append("push {}".format(args[i]))
        code.append("BL {}".format(fCallNode.fname))
        temp = newTempVar()
        code.append("{} = r1".format(temp))
        for arg in args:
            code.append("pop {}".format(arg))
        return temp
    elif factor.type == "var":
        return(factor.node.id[1])

'''
#* generate bexpr
params:
- expr (bexprNode)
- exitLabel (string): label for exit/false
- destLabel (string): label for next destination/true
- negate (bool): if there's a not
return: -
'''
def genBExpr(expr, exitLabel, destLabel, negate):
    if exitLabel != "" and destLabel != "":
        _exit = exitLabel
        _dest = destLabel
    else:
        ifLabel, elseLabel, _ = getIfLabel()
        if expr.bexprEnd is not None:
            _exit = getORLabel()
        else:
            _exit = elseLabel
        _dest = ifLabel
    boolLabel = getBoolLabel()
    code.append("{}:".format(boolLabel))
    genBterm(expr.bterm, _exit, _dest, negate)
    if expr.bexprEnd is not None:
        code.append("{}:".format(_exit))
        genBexprEnd(expr.bexprEnd, elseLabel, ifLabel, negate)

'''
#* generate bexprEnd
params:
- expr (bexprEndNode)
- exitLabel (string): label for exit/false
- destLabel (string): label for next destination/true
- negate (bool): if there's a not
return: -
'''
def genBexprEnd(expr, exitLabel, destLabel, negate):
    if expr.bexprEnd is not None:
        orLabel = getORLabel()
    else:
        orLabel = exitLabel
    genBterm(expr.bterm, orLabel, destLabel, negate)
    if expr.bexprEnd is not None:
        code.append("{}:".format(orLabel))
        genBexprEnd(expr.bexprEnd, exitLabel, destLabel, negate)

'''
#* generate bterm
params:
- term (btermnode)
- exitLabel (string): label for exit/false
- destLabel (string): label for next destination/true
- negate (bool): if there's a not
return: -
'''
def genBterm(term, exitLabel, destLabel, negate):
    if term.btermEnd is not None:
        andLabel = getANDLabel()
    else:
        andLabel = destLabel
    genBfactor(term.bfactor, exitLabel, andLabel, negate)
    if term.btermEnd is not None:
        code.append("{}:".format(andLabel))
        genBterm(term.btermEnd, exitLabel, destLabel, negate)

'''
#* generate bfactor
params:
- factor (bfactorNode)
- exitLabel (string): label for exit/false
- destLabel (string): label for next destination/true
- negate (bool): if there's a not
return: -
'''
def genBfactor(factor, exitLabel, destLabel, negate):
    if factor.bcomp is not None:
        first = genExpr(factor.bcomp.expr1)
        second = genExpr(factor.bcomp.expr2)
        if negate:
            third = destLabel
            fourth = exitLabel
        else:
            third = exitLabel
            fourth = destLabel
        code.append("{} {}, {}, {}".format(
            compOps[factor.bcomp.comp[1]],
            first,
            second,
            third,
        ))
        code.append("b {}".format(fourth))
    elif factor.bfactor is not None:
        _negate = (negate != factor.negate)
        genBfactor(factor.bfactor, exitLabel, destLabel, _negate)
    elif factor.bexpr is not None:
        _negate = (negate != factor.negate)
        genBExpr(factor.bexpr, exitLabel, destLabel, _negate)

'''
#* get or label
params: -
return: or label (string)
'''
def getORLabel():
    global orLabelCount
    orLab = "or_{}".format(orLabelCount)
    orLabelCount += 1
    return orLab

'''
#* get and label
params: -
return: and label (string)
'''
def getANDLabel():
    global andLabelCount
    andLab = "and_{}".format(andLabelCount)
    andLabelCount += 1
    return andLab

'''
#* get if labels
params: -
returns:
- if label (string)
- else label (string)
- end if label (string)
'''
def getIfLabel():
    global ifCount
    ifLab = "if_{}".format(ifCount)
    elseLab = "else_{}".format(ifCount)
    endLab = "endif_{}".format(ifCount)
    ifCount += 1
    return ifLab, elseLab, endLab

'''
#* get previous if labels
params: -
returns:
- previous if label (string)
- previous else label (string)
- previous end if label (string)
'''
def getPrevIfLabel():
    global ifCount
    ifLab = "if_{}".format(ifCount-1)
    elseLab = "else_{}".format(ifCount-1)
    endLab = "endif_{}".format(ifCount-1)
    return ifLab, elseLab, endLab

'''
#* get boolean label
params: -
return: bool label (string)
'''
def getBoolLabel():
    global boolLabelCount
    boolLab = "bool_{}".format(boolLabelCount)
    boolLabelCount += 1
    return boolLab

'''
#* get previous boolean label
params: -
return: prev bool label (string)
'''
def getPrevBoolLabel():
    global boolLabelCount
    boolLab = "bool_{}".format(boolLabelCount-1)
    return boolLab


'''
#* make new temporary variable
params: -
return:
- temp (string): new temp variabe name
'''
def newTempVar():
    global tempCount, localTempCount
    temp = "t{}".format(tempCount)
    tempCount += 1
    localTempCount += 1
    return temp

'''
#* print 3TAC intermediate code
params: 
- code = array of code
return: -
'''
def printFinal(code):
    print("----------")
    print('Final Code')
    for line in code:
        print(line.strip())

'''
#* write code to file
params:
- code: code to write to file
return: -
'''
def outputFile(code):
    output_errors = open('files/intermediate_code.txt', 'w')
    output_errors.writelines("%s\n" % string for string in code)
    output_errors.close()


#* MAIN
generate()