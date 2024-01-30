from txt_handling import read_keywords, read_transition_table
from double_buffer import doubleBuffer

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
RE_DELIM = 20
RE_OPEXPR = 21
RE_OPTERM = 22
RE_PANICDOUBLE = 23
RE_PANICDOUBLEE = 24

RE_STATES = [2, 3, 4, 5, 7, 8, 10, 17, 18, 19, 21, 22, 23, 24]

KEYWORDS = read_keywords()
TRANS_TABLE = read_transition_table()
FINAL_LEXER = []

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

# Example usage:
input_data = open('test cases/Test1.cp', 'r')
# lexer = doubleBuffer(input_data)
test = input_data.read(2048)
print(test)
print(len(test))
# print(test[0:3])
# print(test[3:3])
# print(ord(test[3:3]))
# print(test[3:4])
# print(ord(test[3:4]))
print('-'*10)
# print([ord(c) for c in test])

atest = [ord(c) for c in test]
# print(atest)

# state tracking
curr_state = 0
prev_state = 0

# pointer tracking
curr_point = 0
prev_point = 0

# for c in atest:
# while curr_point < len(atest):
while curr_point < 30:
    c = atest[curr_point]
    prev_state = curr_state
    curr_state = int(TRANS_TABLE[curr_state][c])

    print('c: {} ({}) prev: {} current: {}, p_point: {}, c_point: {}'.format(c, chr(c), prev_state, curr_state, prev_point, curr_point))
    if curr_state == -1:
        curr_state = 0
        print('change curr_state to 0')
        prev_point = curr_point
        curr_point += 1
    elif curr_state == 0:
        # curr_point += 1
        prev_point = curr_point + 1
        curr_point += 1
    elif curr_state == 4:
        print('*'*10)
        print(atest[curr_point])
        print(test[curr_point])
        print('<comp, {}>'.format(test[curr_point]))
        print('*'*10)
        FINAL_LEXER.append('<comp, {}>'.format(test[curr_point]))
        curr_point += 1
        prev_point = curr_point
        curr_state = 0
    elif curr_state == 5:
        print('*'*10)
        print(atest[curr_point])
        print(test[curr_point])
        print('<operator, {}>'.format(test[curr_point]))
        print('*'*10)
        FINAL_LEXER.append('<operator, {}>'.format(test[curr_point]))
        curr_point += 1
        prev_point = curr_point
        curr_state = 0
    elif curr_state == 10:
        print('*'*10)
        print(atest[prev_point:curr_point])
        print(test[prev_point:curr_point])
        print(getKeywordToken(test[prev_point:curr_point], KEYWORDS))
        print('<{}, {}>'.format(getKeywordToken(test[prev_point:curr_point], KEYWORDS), test[prev_point:curr_point]))
        print('*'*10)
        FINAL_LEXER.append('<{}, {}>'.format(getKeywordToken(test[prev_point:curr_point], KEYWORDS), test[prev_point:curr_point]))
        prev_point = curr_point
        # curr_point += 1
        curr_state = 0
    elif curr_state == 18:
        print('*'*10)
        print(atest[prev_point:curr_point])
        print(test[prev_point:curr_point])
        print('<int, {}>'.format(test[prev_point:curr_point]))
        print('*'*10)
        FINAL_LEXER.append('<int, {}>'.format(test[prev_point:curr_point]))
        prev_point = curr_point
        # curr_point += 1
        curr_state = 0
    elif curr_state == 20:
        print('*'*10)
        print(atest[curr_point])
        print(test[curr_point])
        print('<delim, {}>'.format(test[curr_point]))
        print('*'*10)
        FINAL_LEXER.append('<delim, {}>'.format(test[curr_point]))
        curr_point += 1
        prev_point = curr_point
        curr_state = 0
    elif curr_state in RE_STATES:
        prev_point = curr_point
        # curr_point += 1
        curr_state = 0
    else:
        curr_point += 1

print('='*10)
for lex in FINAL_LEXER:
    print(lex)