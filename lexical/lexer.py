from txt_handling import read_keywords, read_transition_table
# from double_buffer import doubleBuffer

# read from keywords and transition table files
KEYWORDS = read_keywords()
TRANS_TABLE = read_transition_table()

# array to store final lexeme token pairs
final_lexer = []
# array to store errors
final_errors = []

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

# line counter for errors
line = 1

# loop through to read code
#TODO currently reading through one array?? read through buffers?
while curr_point < len(atest):
    c = atest[curr_point]
    prev_state = curr_state
    curr_state = int(TRANS_TABLE[curr_state][c])

    # print('c: {} ({}) prev: {} current: {}, p_point: {}, c_point: {}'.format(c, chr(c), prev_state, curr_state, prev_point, curr_point))
    # error state
    if curr_state == -1:
        # print("error line {}: unrecognized character '{}'".format(line, test[curr_point]))
        final_errors.append("error line {}: unrecognized character '{}'\n".format(line, test[curr_point]))
        curr_state = 0
        # print('change curr_state to 0')
        curr_point += 1
        prev_point = curr_point
    # 0 state from 0 state (whitespace)
    elif curr_state == 0:
        prev_point = curr_point + 1
        curr_point += 1
    # <=, <>, >=
    elif curr_state == 2 or curr_state == 3 or curr_state == 7:
        final_lexer.append('<comp, {}>\n'.format(test[prev_point:curr_point+1]))
        curr_point += 1
        prev_point = curr_point
        curr_state = 0
    # <, >
    elif curr_state == 4 or curr_state == 8:
        final_lexer.append('<comp, {}>\n'.format(test[prev_point:curr_point]))
        prev_point = curr_point
        curr_state = 0
    # =
    elif curr_state == 5:
        final_lexer.append('<operator, {}>\n'.format(test[curr_point]))
        curr_point += 1
        prev_point = curr_point
        curr_state = 0
    # identifier
    elif curr_state == 10:
        final_lexer.append('<{}, {}>\n'.format(getKeywordToken(test[prev_point:curr_point], KEYWORDS), test[prev_point:curr_point]))
        prev_point = curr_point
        curr_state = 0
    # double with E
    elif curr_state == 17:
        final_lexer.append('<doubleE, {}>\n'.format(test[prev_point:curr_point]))
        prev_point = curr_point
        curr_state = 0
    # int
    elif curr_state == 18:
        final_lexer.append('<int, {}>\n'.format(test[prev_point:curr_point]))
        prev_point = curr_point
        curr_state = 0
    # double
    elif curr_state == 19:
        final_lexer.append('<double, {}>\n'.format(test[prev_point:curr_point]))
        prev_point = curr_point
        curr_state = 0
    # deliminator
    elif curr_state == 20:
        final_lexer.append('<delim, {}>\n'.format(test[curr_point]))
        curr_point += 1
        prev_point = curr_point
        curr_state = 0
    # +, -
    elif curr_state == 21:
        final_lexer.append('<expr, {}>\n'.format(test[curr_point]))
        curr_point += 1
        prev_point = curr_point
        curr_state = 0
    # /, %, *
    elif curr_state == 22:
        final_lexer.append('<term, {}>\n'.format(test[curr_point]))
        curr_point += 1
        prev_point = curr_point
        curr_state = 0
    # panic state: double . not followed by integer
    elif curr_state == 23:
        final_lexer.append('<double, {}>\n'.format(test[prev_point:curr_point-1]))
        final_lexer.append('<delim, {}>\n'.format(test[curr_point-1]))
        prev_point = curr_point
        curr_state = 0
    # panic state: double E not followed by digit
    elif curr_state == 24:
        final_lexer.append('<double, {}>\n'.format(test[prev_point:curr_point-1]))
        prev_point = curr_point - 1
        curr_state = 0
    # \n to track lines for errors
    elif curr_state == 25:
        line += 1
        prev_point = curr_point + 1
        curr_point += 1
    # handle any unfinished lexemes at the end
    elif curr_point + 1 == len(atest):
        if curr_state == 9:
            final_lexer.append('<{}, {}>\n'.format(getKeywordToken(test[prev_point:], KEYWORDS), test[prev_point:]))
        elif curr_state == 11:
            final_lexer.append('<int, {}>\n'.format(test[prev_point:]))
        elif curr_state == 13:
            final_lexer.append('<double, {}>\n'.format(test[prev_point:]))
        elif curr_state == 14:
            final_lexer.append('<doubleE, {}>\n'.format(test[prev_point:]))
        elif curr_state == 16:
            final_lexer.append('<doubleE, {}>\n'.format(test[prev_point:]))
        curr_point += 1
    # else continue reading
    else:
        curr_point += 1

# print <token, lexeme> pairs and error results
print('='*10)
for lex in final_lexer:
    print(lex.strip())
print('='*10)
for error in final_errors:
    print(error.strip())

# write results to respective output files
# output file for <token, lexeme> pairs
output_lexemes = open('files/lexemes.txt', 'w')
output_lexemes.writelines(final_lexer)
output_lexemes.close()

# output file for errors
output_errors = open('files/errors.txt', 'w')
output_errors.writelines(final_errors)
output_errors.close()