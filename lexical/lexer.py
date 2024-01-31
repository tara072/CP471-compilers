from txt_handling import read_keywords, read_transition_table
# from double_buffer import doubleBuffer

TRANS_TABLE = []
KEYWORDS = []

KEYWORDS = read_keywords()
TRANS_TABLE = read_transition_table()
FINAL_LEXER = []

# checking if identifier string is a keyword or not
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

#* enter code file here!
code_data = open('test cases/Test9.cp', 'r')
# lexer = doubleBuffer(input_data)
#TODO currently reading through entire file, change to read through buffer
test = code_data.read(2048)
print(test)
print(len(test))
print('-'*10)

atest = [ord(c) for c in test]

# state tracking
curr_state = 0
prev_state = 0

# pointer tracking
curr_point = 0
prev_point = 0

# loop through to read code
#TODO currently reading through one array
while curr_point < len(atest):
    c = atest[curr_point]
    prev_state = curr_state
    curr_state = int(TRANS_TABLE[curr_state][c])

    print('c: {} ({}) prev: {} current: {}, p_point: {}, c_point: {}'.format(c, chr(c), prev_state, curr_state, prev_point, curr_point))
    # error state
    if curr_state == -1:
        curr_state = 0
        print('change curr_state to 0')
        curr_point += 1
        prev_point = curr_point
    # 0 state from 0 state (whitespace, \n)
    elif curr_state == 0:
        prev_point = curr_point + 1
        curr_point += 1
    # <=, <>, >=
    elif curr_state == 2 or curr_state == 3 or curr_state == 7:
        print('*'*10)
        print(atest[prev_point:curr_point+1])
        print(test[prev_point:curr_point+1])
        print('<comp, {}>'.format(test[prev_point:curr_point+1]))
        print('*'*10)
        FINAL_LEXER.append('<comp, {}>'.format(test[prev_point:curr_point+1]))
        curr_point += 1
        prev_point = curr_point
        curr_state = 0
    # <, >
    elif curr_state == 4 or curr_state == 8:
        print('*'*10)
        print(atest[prev_point:curr_point])
        print(test[prev_point:curr_point])
        print('<comp, {}>'.format(test[prev_point:curr_point]))
        print('*'*10)
        FINAL_LEXER.append('<comp, {}>'.format(test[prev_point:curr_point]))
        prev_point = curr_point
        curr_state = 0
    # =
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
    # identifier
    elif curr_state == 10:
        print('*'*10)
        print(atest[prev_point:curr_point])
        print(test[prev_point:curr_point])
        print(getKeywordToken(test[prev_point:curr_point], KEYWORDS))
        print('<{}, {}>'.format(getKeywordToken(test[prev_point:curr_point], KEYWORDS), test[prev_point:curr_point]))
        print('*'*10)
        FINAL_LEXER.append('<{}, {}>'.format(getKeywordToken(test[prev_point:curr_point], KEYWORDS), test[prev_point:curr_point]))
        prev_point = curr_point
        curr_state = 0
    # double with E
    elif curr_state == 17:
        print('*'*10)
        print(atest[prev_point:curr_point])
        print(test[prev_point:curr_point])
        print('<doubleE, {}>'.format(test[prev_point:curr_point]))
        print('*'*10)
        FINAL_LEXER.append('<doubleE, {}>'.format(test[prev_point:curr_point]))
        prev_point = curr_point
        curr_state = 0
    # int
    elif curr_state == 18:
        print('*'*10)
        print(atest[prev_point:curr_point])
        print(test[prev_point:curr_point])
        print('<int, {}>'.format(test[prev_point:curr_point]))
        print('*'*10)
        FINAL_LEXER.append('<int, {}>'.format(test[prev_point:curr_point]))
        prev_point = curr_point
        curr_state = 0
    # double
    elif curr_state == 19:
        print('*'*10)
        print(atest[prev_point:curr_point])
        print(test[prev_point:curr_point])
        print('<double, {}>'.format(test[prev_point:curr_point]))
        print('*'*10)
        FINAL_LEXER.append('<double, {}>'.format(test[prev_point:curr_point]))
        prev_point = curr_point
        curr_state = 0
    # deliminator
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
    # +, -
    elif curr_state == 21:
        print('*'*10)
        print(atest[curr_point])
        print(test[curr_point])
        print('<expr, {}>'.format(test[curr_point]))
        print('*'*10)
        FINAL_LEXER.append('<expr, {}>'.format(test[curr_point]))
        curr_point += 1
        prev_point = curr_point
        curr_state = 0
    # /, %, *
    elif curr_state == 22:
        print('*'*10)
        print(atest[curr_point])
        print(test[curr_point])
        print('<term, {}>'.format(test[curr_point]))
        print('*'*10)
        FINAL_LEXER.append('<term, {}>'.format(test[curr_point]))
        curr_point += 1
        prev_point = curr_point
        curr_state = 0
    # panic state: double . not followed by integer
    elif curr_state == 23:
        print('*'*10)
        print('panic!')
        print(atest[prev_point:curr_point])
        print(test[prev_point:curr_point])
        print('<int, {}>'.format(test[prev_point:curr_point-1]))
        print('<delim, {}>'.format(test[curr_point-1]))
        print('*'*10)
        FINAL_LEXER.append('<double, {}>'.format(test[prev_point:curr_point-1]))
        FINAL_LEXER.append('<delim, {}>'.format(test[curr_point-1]))
        prev_point = curr_point
        curr_state = 0
    # panic state: double E not followed by digit
    elif curr_state == 24:
        print('*'*10)
        print('panic!')
        print(atest[prev_point:curr_point])
        print(test[prev_point:curr_point])
        print('<double, {}>'.format(test[prev_point:curr_point-1]))
        print('*'*10)
        FINAL_LEXER.append('<double, {}>'.format(test[prev_point:curr_point-1]))
        prev_point = curr_point - 1
        curr_state = 0
    # handle any unfinished lexemes
    elif curr_point + 1 == len(atest):
        if curr_state == 9:
            print('*'*10)
            print(atest[prev_point:])
            print(test[prev_point:])
            print(getKeywordToken(test[prev_point:], KEYWORDS))
            print('<{}, {}>'.format(getKeywordToken(test[prev_point:], KEYWORDS), test[prev_point:]))
            print('*'*10)
            FINAL_LEXER.append('<{}, {}>'.format(getKeywordToken(test[prev_point:], KEYWORDS), test[prev_point:]))
        elif curr_state == 11:
            print('*'*10)
            print(atest[prev_point:])
            print(test[prev_point:])
            print('<int, {}>'.format(test[prev_point:]))
            print('*'*10)
            FINAL_LEXER.append('<int, {}>'.format(test[prev_point:]))
        elif curr_state == 13:
            print('*'*10)
            print(atest[prev_point:])
            print(test[prev_point:])
            print('<double, {}>'.format(test[prev_point:]))
            print('*'*10)
            FINAL_LEXER.append('<double, {}>'.format(test[prev_point:]))
        elif curr_state == 14:
            print('*'*10)
            print(atest[prev_point:])
            print(test[prev_point:])
            print('<doubleE, {}>'.format(test[prev_point:]))
            print('*'*10)
            FINAL_LEXER.append('<doubleE, {}>'.format(test[prev_point:]))
        elif curr_state == 16:
            print('*'*10)
            print(atest[prev_point:])
            print(test[prev_point:])
            print('<doubleE, {}>'.format(test[prev_point:]))
            print('*'*10)
            FINAL_LEXER.append('<doubleE, {}>'.format(test[prev_point:]))
        curr_point += 1
    # else continue reading
    else:
        curr_point += 1

# print <token, lexeme> pairs from array
#TODO write to file to export
print('='*10)
for lex in FINAL_LEXER:
    print(lex)