from syntax_parser import parse
import symbol_table
import nodes

program, synError = parse()
# array to store errors
final_errors = []
# root symbol table
rootTable = symbol_table.symbolTable("root table")

def analyse():
    if synError:
            # write error to error output file
            outputErrors("Syntax errors, cannot proceed with semantic analysis.")
            print("Syntax errors, cannot proceed with semantic analysis.")
            return

    # analyse declarations
    for dec in program.decls:
        for var in dec.varlist:
            vSym = symbol_table.varSymbol(var.id[1], dec.type[1], var.line)
            if vSym.id not in rootTable.variables:
                rootTable.variables[vSym.id] = vSym
            else:
                print("Multiple declaractions of variable {} at line {}".format(vSym.id, vSym.line))
                final_errors.append("Multiple declaractions of variable {} at line {}".format(vSym.id, vSym.line))
    
    # analyse function declarations
    for fdef in program.fdecls:
        paramTypes = []
        for param in fdef.params:
            paramTypes.append(param.type[1])
        fSym = symbol_table.funcSymbol(
            fdef.fname[1],
            fdef.type[1],
            len(fdef.params),
            paramTypes,
            symbol_table.symbolTable(fdef.fname[1] + " table"),
            fdef.line
        )
        fSym.table.parentTable = rootTable
        
        if fSym.name in rootTable.functions:
            print("Multiple declaractions of function name {} at line {}".format(fSym.name, fSym.line))
            final_errors.append("Multiple declaractions of function name {} at line {}".format(fSym.name, fSym.line))
        else:
            rootTable.functions[fSym.name] = fSym
            for param in fdef.params:
                vSym = symbol_table.varSymbol(param.var.id[1], param.type[1], param.var.line)

                if vSym.id in fSym.table.variables:
                    print("Multiple declaractions of parameter with name {} at line {}".format(vSym.id, vSym.line))
                    final_errors.append("Multiple declaractions of parameter with name {} at line {}".format(vSym.id, vSym.line))
                else:
                    fSym.table.variables[vSym.id] = vSym
            analyseStmts(fdef.stmtSeq, rootTable, fSym)

    # analyse statements (recursively)
    analyseStmts(program.stmtSeq, rootTable, None)

    # wrap up
    printFinals(rootTable, final_errors)
    # write results to error output file
    outputErrors(final_errors)
    return rootTable, program, len(final_errors) > 0

'''
#* analyse statements
params:
- stmtSeq (stmtSeq arrays)
- table (symbolTable)
- funcSym (funcSymbol)
return: -
'''      
def analyseStmts(stmtSeq, table, funcSym):
    if funcSym is None:
        currentTable = table
    else:
        currentTable = funcSym.table

    for stmt in stmtSeq:
        if isinstance(stmt, nodes.assignStmtNode):
            varSym = varLookup(stmt.var.id[1], currentTable)
            if varSym is None:
                print("Assignment before declaration of variable {} at line {}".format(stmt.var.id[1], stmt.var.line))
                final_errors.append("Assignment before declaration of variable {} at line {}".format(stmt.var.id[1], stmt.var.line))
            valid, exprType = evalExpr(stmt.expr, currentTable)
            if not valid:
                print("Invalid statement at line {}".format(stmt.var.line))
                final_errors.append("invalid statement at line {}".format(stmt.var.line))
            if varSym.type != exprType:
                print("Invalid type assigned to variable {} at line {}".format(stmt.var.id[1], stmt.var.line))
                final_errors.append("Invalid type assigned to variable {} at line {}".format(stmt.var.id[1], stmt.var.line))
        elif isinstance(stmt, nodes.ifStmtNode):
            evalBexpr(stmt.bexpr, currentTable)
            analyseStmts(stmt.stmtSeq, currentTable, funcSym)
            if len(stmt.elseStmtSeq) > 0:
                analyseStmts(stmt.elseStmtSeq, currentTable, funcSym)
        elif isinstance(stmt, nodes.whileStmtNode):
            evalBexpr(stmt.bexpr, currentTable)
            analyseStmts(stmt.stmtSeq, currentTable, funcSym)
        elif isinstance(stmt, nodes.builtStmt):
            if stmt.type[1] == "return":
                valid, returnType = evalExpr(stmt.expr, funcSym.table)
                if valid and (returnType != funcSym.returnType):
                    print("Invalid return type {} at line {}".format(returnType, stmt.line))
                    final_errors.append("Invalid return type {} at line {}".format(returnType, stmt.line))
            elif stmt.type[1] == "print":
                evalExpr(stmt.expr, currentTable)

'''
#* evaluate expr
params: 
- expr (exprNode)
- table (symbolTable)
return:
- valid: if the expression is valid (boolean)
- type: expression return type (type/string)
'''
def evalExpr(expr, table):
    valid, termType = evalTerm(expr.term, table)
    if not valid:
        return valid, termType

    if expr.exprEnd is not None:
        valid, endTermType = evalExprEnd(expr.exprEnd, table)
        if termType != endTermType:
            valid = False
            print("Cannot perform {} with two different types at line {}".format(expr.exprEnd.op, expr.exprEnd.line))
            final_errors.append("Cannot perform {} with two different types at line {}".format(expr.exprEnd.op, expr.exprEnd.line))

    return True, termType

'''
#* evaluate exprEnd
params: 
- expr (exprEndNode)
- table (symbolTable)
return:
- valid: if the expression is valid (boolean)
- type: expression return type (type/string)
'''
def evalExprEnd(expr, table):
    valid, termType = evalTerm(expr.term, table)
    if not valid:
        return valid, termType

    if expr.exprE is not None:
        valid, termEndType = evalExprEnd(expr.exprE, table)

        if termType != termEndType:
            valid = False
            print("Cannot perform {} with two different types at line {}".format(expr.exprEnd.op, expr.line))
            final_errors.append("Cannot perform {} with two different types at line {}".format(expr.exprEnd.op, expr.line))
    return valid, termType

'''
#* evaluate term
params: 
- term (termNode)
- table (symbolTable)
return:
- valid: if the term is valid (boolean)
- type: expression return type (type/string)
'''
def evalTerm(term, table):
    valid, factorType = evalFactor(term.factor, table)
    if not valid:
        return valid, factorType
    
    if term.termEnd is not None:
        valid, endFactorType = evalFactor(term.termEnd.factor, table)
        if factorType != endFactorType:
            valid = False
            print("Cannot perform {} with two different types at line {}".format(term.termEnd.op, term.line))
            final_errors.append("Cannot perform {} with two different types at line {}".format(term.termEnd.op, term.line))
    return valid, factorType

'''
#* evaluate factor
params: 
- factor (factorNode)
- table (symbolTable)
return:
- valid: if the factor is valid (boolean)
- type: expression return type (type/string)
'''
def evalFactor(factor, table):
    if factor.type == "number":
        if factor.node[0] == "int":
            return True, "int"
        elif factor.node[0] == "double":
            return True, "double"
    elif factor.type == "expr":
        return evalExpr(factor.node, table)
    elif factor.type == "funcCall":
        fCallNode = factor.node
        funcSym = funcLookup(fCallNode.fname, table)
        if funcSym is None:
            print("Function {} called but not declared at line {}".format(fCallNode.fname, fCallNode.line))
            final_errors.append("Function {} called but not declared at line {}".format(fCallNode.fname, fCallNode.line))
            return False, "UNDEFINED" # TODO: figure out what I want to return
        else:
            if len(fCallNode.exprSeq) != funcSym.paramCount:
                print("Expected {} parameters but recieved {} at line {}".format(funcSym.paramCount, len(fCallNode.exprSeq), fCallNode.line))
                final_errors.append("Expected {} parameters but recieved {} at line {}".format(funcSym.paramCount, len(fCallNode.exprSeq), fCallNode.line))
            isRight = True
            for index in range(len(fCallNode.exprSeq)):
                valid, paramType = evalExpr(fCallNode.exprSeq[index], table)
                if not valid:
                    print("Invalid parameter at line {}".format(fCallNode.line))
                    final_errors.append("Invalid parameter at line {}".format(fCallNode.line))
                    isRight = False
                if paramType != funcSym.paramTypes[index]:
                    print("Wrong parameter type, expected {} but recieved {} at line {}".format(funcSym.paramTypes[index], paramType, fCallNode.line))
                    final_errors.append("Wrong parameter type, expected {} but recieved {} at line {}".format(funcSym.paramTypes[index], paramType, fCallNode.line))
            return isRight, funcSym.returnType
    elif factor.type == "var":
        varSym = varLookup(factor.node.id[1], table)
        if varSym is not None:
            return True, varSym.type
        else:
            print("Undeclared variable {} at line {}".format(factor.node.id[1], factor.node.line))
            final_errors.append("Undeclared variable {} at line {}".format(factor.node.id[1], factor.node.line))
    return False, "UNDEFINED"

'''
#* evaluate bexpr
params: 
- bexpr (bexprNode)
- table (symbolTable)
return:
- valid: if the expression is valid (boolean)
- type: expression return type (type/string)
'''
def evalBexpr(bexpr, table):
    valid = evalBterm(bexpr.bterm, table)
    if bexpr.bexprEnd is not None:
        valid = evalBexpr(bexpr.bexprEnd, table)
    return valid

'''
#* evaluate bterm
params: 
- bterm (btermNode)
- table (symbolTable)
return:
- valid: if the expression is valid (boolean)
- type: expression return type (type/string)
'''
def evalBterm(bterm, table):
    valid = evalBfactor(bterm.bfactor, table)
    if bterm.btermEnd is not None:
        valid = evalBterm(bterm.btermEnd, table)
    return valid

'''
#* evaluate bfactor
params: 
- bfactor (bfactorNode)
- table (symbolTable)
return:
- valid: if the expression is valid (boolean)
- type: expression return type (type/string)
'''
def evalBfactor (bfactor, table):
    if bfactor.bfactor is not None:
        return evalBfactor(bfactor.bfactor, table)
    
    if bfactor.bexpr is not None:
        return evalBexpr(bfactor.bexpr, table)
    
    valid = True
    if bfactor.bcomp is not None:
        valid1, type1 = evalExpr(bfactor.bcomp.expr1, table)
        valid2, type2 = evalExpr(bfactor.bcomp.expr2, table)
        valid = valid1 and valid2 and type1 == type2
        if type1 != type2:
            print("Cannot perform comparison with two different types at line {}".format(bfactor.bcomp.comp[2]))
            final_errors.append("Cannot perform comparison with two different types at line {}".format(bfactor.bcomp.comp[2]))

    return valid


'''
#* variable lookup
helper function to reduce reptitive code
look to see if a variable has been declared 
if not declared in initial table, then check parent tables until None
params:
- table: table to lookup in (symbol table)
- varName: variable name to lookup (string)
return:
- declared variable (varSymbol)
- None, if variable has not been declared
'''
def varLookup(varName, table):
    current = table
    while current is not None:
        if varName not in current.variables:
            current = current.parentTable
        else:
            return current.variables[varName]
    return None

'''
#* function lookup
helper function to reduce reptitive code
look to see if a function has been declared 
if not declared in initial table, then check parent tables until None
params:
- table: table to lookup in (symbol table)
- funcName: function name to lookup (string)
return:
- declared function (funcSymbol)
- None, if variable has not been declared
'''
def funcLookup(funcName, table):
    current = table
    while current is not None:
        if funcName not in current.functions:
            current = current.parentTable
        else:
            return current.functions[funcName]
    return None

'''
#* print results from program and final_errors array
params: 
- rootTable = root symbol table
- final_errors = array of errors
return: -
'''
def printFinals(rootTable, final_errors):
    print('Final Table')
    print(rootTable)
    print('~'*10)
    print('Final Errors')
    for error in final_errors:
        print(error.strip())

'''
#* write final_errors array to error file
params:
- errs: errors to write to file
return: -
'''
def outputErrors(errs):
    output_errors = open('files/sem_errors.txt', 'w')
    output_errors.writelines(errs)
    output_errors.close()

#* MAIN
# analyse()