from analyser import analyse
import nodes

rootTable, program, semErr = analyse()
code = [] #3TAC generated code - a list for now cause idk

# track counts for labels, registers and temp values
labelCount = 1
regCount = 1
tempCount = 1

def generate():
    if semErr:
            # write error to error output file
            if isinstance(semErr, str):
                print(semErr)
                outputErrors(semErr)
                return None, semErr
            else:
                outputErrors("Semantic errors, cannot proceed with intermediate code generation.")
                print("Semantic errors, cannot proceed with intermediate code generation.")
            return None, "Semantic errors, cannot proceed with intermediate code generation."
    
    print(rootTable)    
    # print(program)

    # generate function declarations
    if len(rootTable.functions) > 0:
        code.append("B main")
        # go through functions
        for func in program.fdecls:
            # print(func)
            funcTable = rootTable.functions[func.fname[1]]
            code.append(func.fname[1] + ":")
            code.append("begin " + str(len(funcTable.table.variables) * 4))
            # double check if I just do these pushes every time or not ..
            code.append("push LR")
            # go through params
            paramPoint = 4
            for param in func.params:
                paramPoint += 4
                code.append("{} = [sp + {}]".format(param.var.id[1], paramPoint))
            genStmts(func.stmtSeq)
            #! is this supposed to always be at the end of a function??
            code.append("pop {PC}")
    
    code.append("main:")
    #! why is this begin 48??????
    code.append("begin " + str(len(rootTable.variables) * 4))

    # generate statements
    genStmts(program.stmtSeq)
    printFinal(code)
    return code
'''
#* generate statements
params:
- stmtSeq (stmtSeq arrays)
return: -
'''
def genStmts(stmtSeq):
    global labelCount, regCount
    for index, stmt in enumerate(stmtSeq):
        if isinstance(stmt, nodes.assignStmtNode):
            first = stmt.var.id[1]
            second = genExpr(stmt.expr)
            print("ASSIGN STMT NODE")
            code.append("{} = {}".format(first, second))
        elif isinstance(stmt, nodes.ifStmtNode):
            ifStr = ""
            bcomp = stmt.bexpr.bterm.bfactor.bcomp
            #TODO: make this a map?
            if bcomp.comp[1] == ">":
                ifStr += "BGT"
            elif bcomp.comp[1] == "<":
                ifStr += "BLT"
            elif bcomp.comp[1] == ">=":
                ifStr += "BGE"
            elif bcomp.comp[1] == "<=":
                ifStr += "BLE"
            elif bcomp.comp[1] == "<>":
                ifStr += "BNE"
            elif bcomp.comp[1] == "==":
                ifStr += "BEQ"
            ifStr += " {}, {}, label{}".format(
                bcomp.expr1.term.factor.node.id[1],
                bcomp.expr2.term.factor.node.id[1],
                labelCount
            )
            code.append(ifStr)
            code.append("label{}:".format(labelCount))
            labelCount += 1
            genStmts(stmt.stmtSeq)
            if len(stmt.elseStmtSeq) > 0:
                code.append("B label{}".format(labelCount + 1))
                code.append("label{}:".format(labelCount))
                labelCount += 1
                genStmts(stmt.elseStmtSeq)
            if len(stmtSeq)-1 != index:
                code.append("label{}:".format(labelCount))
                labelCount += 1
        elif isinstance(stmt, nodes.whileStmtNode):
            # TODO: while statement
            print(stmt)
            print("WHILE STATEMENT")
        elif isinstance(stmt, nodes.builtStmt):
            if stmt.type[1] == "return":
                second = genExpr(stmt.expr)
                code.append("r{} = {}".format(regCount, second))
            elif stmt.type[1] == "print":
                second = genExpr(stmt.expr)
                code.append("print {}".format(second))
'''
#* generate expr
params:
- expr (exprNode)
return: 
- exprLine (string): line of code
'''
def genExpr(expr):
    print("GEN EXPR")
    print(expr)
    exprLine = ""
    exprLine += genTerm(expr.term)
    if expr.exprEnd is not None:
        #! what is supposed to happen in this case? 
        exprLine += genExprEnd(expr.exprEnd)
    print(exprLine)
    return exprLine

'''
#* generate exprEnd
params:
- expr (exprEndNode)
return:
- exprLine ()
'''
def genExprEnd(expr):
    global tempCount
    print("GEN EXPREND")
    print(expr)
    term = genTerm(expr.term)
    print("{} {}".format(expr.op[1], term))
    if expr.exprE is not None:
        print("DO ANOTHER EXPREND")
        # TODO: figure out what to do here
        # print(expr.exprE)
        # genExprEnd(expr.exprE)
        # print(genExprEnd(expr.exprE))
        # print("t{} = t{} {} {}".format(tempCount, tempCount-1, expr.op[1], term))
        # code.append("t{} = t{} {} {}".format(tempCount, tempCount-1, expr.op[1], term))
        # tempCount += 1
        # return genExprEnd(expr.exprE)
        # return (" {} t{}".format(expr.op[1], tempCount-1))
    return (" {} {}".format(expr.op[1], term))

'''
#* generate term
params:
- term (termnode)
return:
- termLine ()
'''
def genTerm(term):
    print("GEN TERM")
    print(term)
    termLine = ""
    termLine += genFactor(term.factor)
    if term.termEnd is not None:
        print(term.termEnd)
        termLine += genTermEnd(term.termEnd)
    return termLine

'''
#* generate termEnd
params:
- term (termEndNode)
return:
- termLine ()
'''
def genTermEnd(term):
    global tempCount
    print("GEN TERMEND")
    print(term)
    factor = genFactor(term.factor)
    print("{} {}".format(term.op[1], factor))
    if term.termE is not None:
        print("DO ANOTHER EXPREND")
        # TODO: figure out what to do here
        # print(expr.exprE)
        # genExprEnd(expr.exprE)
        # print(genExprEnd(expr.exprE))
        # print("t{} = t{} {} {}".format(tempCount, tempCount-1, expr.op[1], term))
        # code.append("t{} = t{} {} {}".format(tempCount, tempCount-1, expr.op[1], term))
        # tempCount += 1
        # return genExprEnd(expr.exprE)
        # return (" {} t{}".format(expr.op[1], tempCount-1))
    return (" {} {}".format(term.op[1], factor))

'''
#* generate factor
params:
- factor (factorNode)
return:
- factorLine (string)
'''
def genFactor(factor):
    global tempCount
    print("GEN FACTOR")
    print(factor)
    if factor.type == "number":
        code.append("t{} = {}".format(tempCount, factor.node[1]))
        tempCount += 1
        return("t{}".format(tempCount-1))
    elif factor.type == "expr":
        return genExpr(factor.node)
    elif factor.type == "funcCall":
        fCallNode = factor.node
        print("GEN FACTOR FCALLNODE")
        print(fCallNode)
        #TODO: push params and call function
        # code.append("BL {}".format(fCallNode.fname))
        return("\nBL {}".format(fCallNode.fname))
    elif factor.type == "var":
        return(factor.node.id[1])

# TODO: statements: while loops, factor: function calls
# TODO: bexpr, bterm, bfactor
# TODO: figure out more than 1 exprEnd or termEnd (z=2+3+4 or z=2*3*4)

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
def outputErrors(code):
    output_errors = open('files/intermediate_code.txt', 'w')
    output_errors.writelines(code)
    output_errors.close()


#* MAIN
generate()