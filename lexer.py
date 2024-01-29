from txt_handling import read_keywords, read_transition_table

TRANS_TABLE = []
KEYWORDS = []

# return states
RE_LE = 2
RE_NE = 3
RE_LT = 4
RE_EQ = 5
RE_GE = 7
RE_GT = 8
RE_IDENT = 10
RE_DOUBLEE = 17
RE_INT = 18
RE_DOUBLE = 19
RE_DELIM = 21

KEYWORDS = read_keywords()
TRANS_TABLE = read_transition_table()

# checking if identifier string is a keyword
def getKeywordToken(keyword, keyArray): 
    is_keyword = False
    token = ''
    i = 0
    while not is_keyword and i < len(keyArray):
        j = 1
        while not is_keyword and j < len(keyArray[i]):
            if keyword.strip().lower() == keyArray[i][j]:
                is_keyword = True
                token = keyArray[i][0]
            else: j += 1
        i += 1
    if not is_keyword: token = 'identifier'
    return (token)

# print(getKeywordToken('def', KEYWORDS))