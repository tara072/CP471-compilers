# root node
class Program:
    def __init__(self):
        # these will be used to store the nodes for each branch
        self.fdecls = []
        self.decls = [] #declNodes
        self.stmtSeq = []

    def __str__(self):
        fdeclsStr = ""
        for node in self.fdecls:
            fdeclsStr += '{} '.format(node)

        declsStr = ""
        for node in self.decls:
            declsStr += '\n{}'.format(node)

        stmtStr = ""
        for node in self.stmtSeq:
            stmtStr += '\n{}'.format(node)

        return('''******
PROGRAM:
======
FDECLS: {}
======
DECLS: {}
======
STMTSEQ: {}
******'''.format(fdeclsStr, declsStr, stmtStr))

# NODES
'''
#* fdef node
    - type ("int" or "double")
    - fname = function name / identifier
    - params = list of param nodes
    - decls = declarations in the function (declNode)
    - stmtSeq = list of statements
'''
class fdefNode:
    def __init__(self):
        self.type = None
        self.fname = None
        self.params = []
        self.decls = [] 
        self.stmtSeq = []
        self.line = 0

    def __str__(self):
        paramsStr = ''
        for node in self.params:
            paramsStr += '{}'.format(node)
        declsStr = ''
        for node in self.decls:
            declsStr += '{}'.format(node)
        stmtStr = ''
        for node in self.stmtSeq:
            stmtStr += '{}'.format(node)
        return('''fdefNode:
    fdefNode/type:
    --> type/{}
    fdefNode/fname:
    --> fname/{}
    fdefNode/params:
    --> params/{}
    fdefNode/decls:
    --> decls/{}
    fdefNode/stmtSeq:
    --> stmtSeq/{}'''.format(self.type, self.fname, paramsStr, declsStr, stmtStr))

'''
#* param node
    - type (token)
    - var (var node)
'''
class paramNode:
    def __init__(self):
        self.type = None
        self.var = None

    def __str__(self):
        return('''paramNode:
    paramNode/type:
    --> type/{}
    paramNode/var:
    --> var/{} '''.format(self.type, self.var))
    

'''
#* decl node
    - type (token)
    - varlist (list of var nodes)
'''
class declNode:
    def __init__(self):
        self.type = []
        self.varlist = []
        self.line = 0
    
    def __str__(self):
        varStr = ''
        for node in self.varlist:
            varStr += '{}'.format(node)
        return('''declNode:
    declNode/type:
    --> type/{}
    declNode/line:
    --> line/{}
    declNode/varlist:
    --> varlist/{}'''.format(self.type, self.line, varStr))

'''
#* var node
    - id = identifier (token)
    - varEnd (var end node)
'''
class varNode:
    def __init__(self, token):
        self.id = token[:2]
        self.line = token[2]

    def __str__(self):
        return('varNode: {} '.format(self.id))

'''
#* var end node
    - expr (expr node)
'''
class varEndNode:
    def __init__(self, exprNode):
        self.expr = exprNode
    
    def __str__(self):
        return('''varEndNode:
    varEndNode/expr
    --> expr/{} '''.format(self.expr))

'''
#* expr node
<expr> ::= <expr> + <term> | <expr> - <term> | <term>
<exprEnd> ::= + <term> <exprEnd> | - <term> <exprEnd> | e
    - term (term node)
    - exprEnd (exprEnd node)
'''
class exprNode:
    def __init__(self):
        self.term = None
        self.exprEnd = None
        self.line = 0
    
    def __str__(self):
        return('''exprNode:
    exprNode/term:
    --> term/{}
    exprNode/exprEnd: 
    --> exprEnd/{} '''.format(self.term, self.exprEnd))

'''
#* exprEnd node
    - op = addition/subtraction (token type)
    - term (termNode)
    - exprE (exprEndNode)
'''
class exprEndNode:
    def __init__(self):
        self.op = ''
        self.term = None
        self.exprE = None
        self.line = 0

    def __str__(self):
        return ('''exprEndNode:
    exprEndNode/op:
    --> op/{}
    exprEndNode/term:
    --> term/{}
    exprEndNode/exprEnd:
    --> exprEnd/{} '''.format(self.op, self.term, self.exprE))

'''
#* term node
    - factor (factor node)
    - termEnd (term end node)
'''
class termNode:
    def __init__(self):
        self.factor = None
        self.termEnd = None
        self.line = 0
    
    def __str__(self):
        return('''termNode:
    termNode/line: {}
    termNode/factor:
    --> factor/{}
    termNode/termEnd:
    --> termEnd/{} '''.format(self.line, self.factor, self.termEnd))

'''
#* term end node
<termEnd> ::= * <factor> | / <factor> | % <factor> | e
    - op (token type)
    - factor (factor node)
'''
class termEndNode:
    def __init__(self):
        self.op = ''
        self.factor = None
        self.termE = None
    
    def __str__(self):
        return('''termEndNode:
    termEndNode/op:
    --> op/{}
    termEndNode/factor:
    --> factor/{} '''.format(self.op, self.factor))

'''
#* factor node
<factor> ::= <var> | <number> | (<expr>) | <fname>(<exprseq>)
    - type = factor type (var, number, expr, function) (token type / stirng)
    - node = node of factor? (varNode, ?, exprNode, or fdefNode?)
    - negative = if it's a negative (for numbers)

'''
class factorNode:
    def __init__(self):
        self.type = ""
        self.node = None
        self.negative = False
        self.line = 0
    
    def __str__(self):
        return('''factorNode:
    factorNode/type: {}
    factorNode/negative: {}
    factorNode/node:
    --> node/{} '''.format(self.type, self.negative, self.node))
    
'''
#* assignment statement node
<stmt> := <var> = <expr>
    - var (varNode)
    - expr (exprNode)
'''
class assignStmtNode:
    def __init__(self, var, expr):
        self.var = var
        self.expr = expr
    
    def __str__(self):
        return('''\n-----------
assignStmtNode:
    assignStmt/var:
    --> var/{}
    assignStmt/expr:
    --> expr/{}
-----------'''.format(self.var, self.expr))

'''
#* if statement node
<stmt> := if <bexpr> then <statement_seq> fi | 
        if <bexpr> then <statement_seq> else <statement_seq> fi
    - bexpr (bexprNode)
    - stmtSeq = array of statements
    - elseStmtSeq = array of else statements 
'''
class ifStmtNode:
    def __init__(self, bexpr, stmtSeq, elseStmtSeq):
        self.bexpr = bexpr
        self.stmtSeq = stmtSeq
        self.elseStmtSeq = elseStmtSeq
    
    def __str__(self):
        stmtStr = ''
        for stmt in self.stmtSeq:
            stmtStr += '{}'.format(stmt)
        elseStmtStr = ''
        for stmt in self.elseStmtSeq:
            elseStmtStr += '{}'.format(stmt)
        return ('''\n-----------
ifStmtNode:
    ifStmt/bexpr:
    --> bexpr/{}
    ifStmt/stmtSeq:
    --> stmtSeq/{}
    ifStmt/elseStmtSeq:
    --> elseStmtSeq/{}
-----------'''.format(self.bexpr, stmtStr, elseStmtStr))

'''
#* while statement node
while <bexpr> do <statement_seq> od
    - bexpr (bexprNode)
    - stmtSeq = list of statements (list)
'''
class whileStmtNode:
    def __init__(self, bexpr, stmtSeq):
        self.bexpr = bexpr
        self.stmtSeq = stmtSeq
    
    def __str__(self):
        stmtStr = ''
        for stmt in self.stmtSeq:
            stmtStr += '{}'.format(stmt)
        return ('''\n-----------
whileStmtNode:
    whileStmt/bexpr:
    --> bexpr/{}
    ifStmt/stmtSeq:
    --> stmtSeq/{}
-----------'''.format(self.bexpr, stmtStr))
    
'''
#* built in statement node
print <expr> | return <expr>
    - type = token type / print or return (token / string)
    - expr (exprNode)
'''
class builtStmt:
    def __init__(self, tokenType, expr, line):
        self.type = tokenType
        self.expr = expr
        self.line = line
    
    def __str__(self):
        return('''\n-----------
buildStmt:
    buildStmt/type:
    --> type/{}
    buildStmt/expr:
    --> expr/{}
-----------'''.format(self.type, self.expr))

'''
#* bexpr node
<bexpr> ::= <bexpr> or <bterm> | <bterm>
<bexpr> := <bterm> <bexprEnd>
'''
class bexprNode:
    def __init__(self):
        self.bterm = ''
        self.bexprEnd = None

    def __str__(self):
        return('''bexprNode:
    bexprNode/bterm:
    --> bterm/{}
    bexprNode/bexprEnd:
    --> bexprEnd/{} '''.format(self.bterm, self.bexprEnd))

'''
#* bexpr end node
<bexprEnd> := or <bterm> <bexprEnd> | e
'''
class bexprEndNode:
    def __init__(self):
        self.bterm = None
        self.bexprEnd = None

    def __str__(self):
        return('''bexprEndNode:
    bexprEnd/bterm:
    --> bterm/{}
    bexprEnd/bexprEnd:
    --> bexprEnd/{} '''.format(self.bterm, self.bexprEnd))

'''
#* bterm node
<bterm> and <bfactor> | <bfactor>
<bterm> := <bfactor> <btermEnd>
    - bfactor (bfactorNode)
    - btermEnd (btermEndNode)
'''
class btermNode:
    def __init__(self):
        self.bfactor = None
        self.btermEnd = None
    
    def __str__(self):
        return('''btermNode:
    btermNode/bfactor:
    --> bfactor/{}
    btermNode/btermEnd:
    --> btermEnd/{} '''.format(self.bfactor, self.btermEnd))

'''
#* bterm end node
<btermEnd> := and <factor> | e
'''
class btermEndNode:
    def __init__(self):
        self.bfactor = None
        self.btermEnd = None

    def __str__(self):
        return('''btermEndNode:
    btermEnd/bfactor:
    --> bfactor/{}
    btermEnd/btermEnd:
    --> btermEnd/{} '''.format(self.bfactor, self.btermEnd))

'''
#* bfactor node
<bfactor> := not (<bcomp>)
'''
class bfactorNode:
    def __init__(self):
        self.negate = None
        self.bfactor = None
        self.bcomp = None
        self.bexpr = None
    
    def __str__(self):
        return('''bfactorNode:
    bfactorNode/negate:
    --> negate/{}
    bfactorNode/bfactor: 
    --> bfactor/{}
    bfactorNode/bcomp:
    --> bcomp/{}
    bfactorNode/bexpr:
    --> bexpr/{}'''.format(self.negate, self.bfactor, self.bcomp, self.bexpr))
    
'''
#* bcomp node
<bcomp> := <expr> <comp> <expr>
    - expr1 (exprNode)
    - comp (list)
    - expr2 (exprNOde)
'''
class bcompNode:
    def __init__(self, expr1, comp, expr2):
        self.comp = comp
        self.expr1 = expr1
        self.expr2 = expr2
        self.line = 0

    def __str__(self):
        return('''bcompNode:
    bcompNode/expr1:
    --> expr1/{}
    bcompNode/comp: {}
    bcompNode/expr2:
    --> expr2/{} '''.format(self.expr1, self.comp, self.expr2))

'''
#* function call node
    - fname (string)
    - exprSeq = list of exprSeqNode
'''
class fCallNode:
    def __init__(self):
        self.fname = ""
        self.exprSeq = []
        self.line = 0
    
    def __str__(self):
        exprStr = ''
        for node in self.exprSeq:
            exprStr += '{}'.format(node)
        return('''fCallNode:
    fCallNode/fname:
    --> fname: {}
    fCallNode/exprSeq:
    --> exprSeq: {}'''.format(self.fname, exprStr))
    