'''
#* symbol table
    - variables: variables declared (map)
    - functions: functions declared (map)
    - parentTable (symbolTable)
'''
class symbolTable:
    def __init__(self, tableId):
        self.id = tableId
        self.variables = {}
        self.functions = {}
        self.parentTable = None
    
    def __str__(self):
        varStr = ""
        for key, var in self.variables.items():
            varStr += '''
    key: {}
    {}'''.format(key, var)

        funcStr = ""
        for key, var in self.functions.items():
            funcStr += '''
    key: {}
    {}'''.format(key, var)
            
        if self.parentTable is None:
            ptStr = None
        else:
            ptStr = self.parentTable.id

        return('''******
{}:
-------
variables: {}
-------
functions: {}
-------
parentTable: {}
-------
******'''.format(self.id, varStr, funcStr, ptStr))

'''
#* variable symbol
    - lexeme: value (string)
    - type: int or double (string / type)
    - line: line number (int)
'''
# variable
class varSymbol:
    def __init__(self, lex, dataType, line, varType):
        self.id = lex #string
        self.type = dataType #type
        self.line = line #int
        self.varType = varType #param or variable

    def __str__(self):
        return ('''varSymbol:
    id: {}
    type: {}
    line: {}
    varType: {}
'''.format(self.id, self.type, self.line, self.varType))

'''
#* function symbol
    - name: function name (string)
    - returnType (type / string)
    - paramCount (int)
    - paramTypes (list of types)
    - table: parent table (symbolTable)
    - line: line number (int)
'''
# function
class funcSymbol:
    def __init__(self, name, returnType, paramCount, paramTypes, table, line):
        self.name = name #string
        self.returnType = returnType #type
        self.paramCount = paramCount #int
        self.paramTypes = paramTypes #list of types
        self.table = table #symbolTable
        self.line = line #int

    def __str__(self):
        return ('''funcSymbol:
    name: {}
    returnType: {}
    paramCount: {}
    paramTypes: {}
    line: {}
    table:
{}
'''.format(self.name, self.returnType, self.paramCount, self.paramTypes, self.line, self.table))