from txt_handling import read_keywords, read_transition_table

# read from keywords and transition table files
KEYWORDS = read_keywords()
TRANS_TABLE = read_transition_table()

# array to store final lexeme token pairs
final_lexer = []
# array to store errors
final_errors = []
# array for parser lexeme token pairs
final_array_lexer = []

#* enter code file here!
code_data = open('test cases/Test9.cp', 'r')

# # state tracking
curr_state = 0
prev_state = 0

# line counter for errors
line = 1

# buffers for double buffer method
buffA = []
buffB = []

# buffer tracking
currBuff = 0 # current buffer tracker
contBuff = False # continue reading in next buffer
cont_point = 0 # point where the continued string starts in the last buffer

# buffer size
BUFFER_SIZE = 2048

'''
#* checking if identifier string is a keyword or not
params: keyword = identifier string, keyArray = array of keywords
return: token = keyword or "identifier" (string)
'''
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

'''
#* fill buffer with characters
params: code = the code file (open file)
return: filled buffer (array)
'''
def fillBuffer(code):
    data = code.read(BUFFER_SIZE)
    if not data:
        return -1
    else: 
        buffer = [ord(c) for c in data]
        test = ''.join(chr(c) for c in buffer)
        return buffer

'''
#* loop to read the code characters in the buffer
adds the resulting token, lexeme pairs to the final_lexer array and final_array_lexer
adds errors to final_errors array
params: buffer = the buffer to read from (array)
return: -
'''
def readBuffer(buffer):
    # state tracking
    global curr_state, prev_state

    # pointer tracking
    curr_point = 0
    prev_point = 0

    # line counter for errors
    global line

    # buffer tracking (if overflowing buffer)
    global contBuff, cont_point

    while curr_point < len(buffer):
        c = buffer[curr_point]
        prev_state = curr_state
        curr_state = int(TRANS_TABLE[curr_state][c])

        # print('c: {} ({}) prev: {} current: {}, p_point: {}, c_point: {}'.format(c, chr(c), prev_state, curr_state, prev_point, curr_point))

        # error state
        if curr_state == -1:
            final_errors.append("error line {}: unrecognized character '{}'\n".format(line, ''.join(chr(buffer[curr_point]))))
            curr_state = 0
            curr_point += 1
            prev_point = curr_point
        # 0 state from 0 state (whitespace)
        elif curr_state == 0:
            prev_point = curr_point + 1
            curr_point += 1
        # <=, <>, >=
        elif curr_state == 2 or curr_state == 3 or curr_state == 7:
            if contBuff:
                if currBuff == 0:
                    fullLex = buffB[cont_point:] + buffA[:curr_point]
                else: 
                    fullLex = buffA[cont_point:] + buffB[:curr_point]
                    
                final_lexer.append('<comp, {}>\n'.format(''.join(chr(c) for c in fullLex)))
                final_array_lexer.append(['comp', chr(fullLex), line])
                contBuff = False
                cont_point = 0
            else:
                final_lexer.append('<comp, {}>\n'.format(''.join(chr(c) for c in buffer[prev_point:curr_point+1])))
                final_array_lexer.append(['comp', ''.join(chr(c) for c in buffer[prev_point:curr_point+1]), line])
            curr_point += 1
            prev_point = curr_point
            curr_state = 0
        # <, >
        elif curr_state == 4 or curr_state == 8:
            if contBuff:
                if currBuff == 0:
                    fullLex = buffB[cont_point:] + buffA[:curr_point]
                else: 
                    fullLex = buffA[cont_point:] + buffB[:curr_point]
                    
                final_lexer.append('<comp, {}>\n'.format(''.join(chr(c) for c in fullLex)))
                final_array_lexer.append(['comp', chr(fullLex), line])
                contBuff = False
                cont_point = 0
            else:
                final_lexer.append('<comp, {}>\n'.format(''.join(chr(c) for c in buffer[prev_point:curr_point])))
                final_array_lexer.append(['comp', ''.join(chr(c) for c in buffer[prev_point:curr_point]), line])
            prev_point = curr_point
            curr_state = 0
        # =
        elif curr_state == 5:
            final_lexer.append('<operator, {}>\n'.format(''.join(chr(buffer[curr_point]))))
            final_array_lexer.append(['operator', chr(buffer[curr_point]), line])
            curr_point += 1
            prev_point = curr_point
            curr_state = 0
        # identifier
        elif curr_state == 10:
            if contBuff:
                if currBuff == 0:
                    fullLex = buffB[cont_point:] + buffA[:curr_point]
                else: 
                    fullLex = buffA[cont_point:] + buffB[:curr_point]
                    
                final_lexer.append('<{}, {}>\n'.format(
                    getKeywordToken(''.join(chr(c) for c in fullLex), KEYWORDS),
                    ''.join(chr(c) for c in fullLex)
                ))
                final_array_lexer.append([
                    getKeywordToken(''.join(chr(c) for c in fullLex), KEYWORDS),
                    chr(fullLex),
                    line
                ])
                contBuff = False
                cont_point = 0
            else:
                final_lexer.append('<{}, {}>\n'.format(
                    getKeywordToken(''.join(chr(c) for c in buffer[prev_point:curr_point]), KEYWORDS),
                    ''.join(chr(c) for c in buffer[prev_point:curr_point])
                ))
                final_array_lexer.append([
                    getKeywordToken(''.join(chr(c) for c in buffer[prev_point:curr_point]), KEYWORDS),
                    ''.join(chr(c) for c in buffer[prev_point:curr_point]),
                    line
                ])
            prev_point = curr_point
            curr_state = 0
        # double with E
        elif curr_state == 17:
            if contBuff:
                if currBuff == 0:
                    fullLex = buffB[cont_point:] + buffA[:curr_point]
                else: 
                    fullLex = buffA[cont_point:] + buffB[:curr_point]
                    
                final_lexer.append('<doubleE, {}>\n'.format(''.join(chr(c) for c in fullLex)))
                final_array_lexer.append(['doubleE', ''.join(chr(c) for c in fullLex), line])
                contBuff = False
                cont_point = 0
            else:
                final_lexer.append('<doubleE, {}>\n'.format(''.join(chr(c) for c in buffer[prev_point:curr_point])))
                final_array_lexer.append(['doubleE', ''.join(chr(c) for c in buffer[prev_point:curr_point]), line])
            prev_point = curr_point
            curr_state = 0
        # int
        elif curr_state == 18:
            if contBuff:
                if currBuff == 0:
                    fullLex = buffB[cont_point:] + buffA[:curr_point]
                else: 
                    fullLex = buffA[cont_point:] + buffB[:curr_point]
                    
                final_lexer.append('<int, {}>\n'.format(''.join(chr(c) for c in fullLex)))
                final_array_lexer.append(['int', ''.join(chr(c) for c in fullLex), line])
                contBuff = False
                cont_point = 0
            else:
                final_lexer.append('<int, {}>\n'.format(''.join(chr(c) for c in buffer[prev_point:curr_point])))
                final_array_lexer.append(['int', ''.join(chr(c) for c in buffer[prev_point:curr_point]), line])
            prev_point = curr_point
            curr_state = 0
        # double
        elif curr_state == 19:
            if contBuff:
                if currBuff == 0:
                    fullLex = buffB[cont_point:] + buffA[:curr_point]
                else: 
                    fullLex = buffA[cont_point:] + buffB[:curr_point]
                    
                final_lexer.append('<double, {}>\n'.format(''.join(chr(c) for c in fullLex)))
                final_array_lexer.append(['double', ''.join(chr(c) for c in fullLex), line])
                contBuff = False
                cont_point = 0
            else:
                final_lexer.append('<double, {}>\n'.format(''.join(chr(c) for c in buffer[prev_point:curr_point])))
                final_array_lexer.append(['double', ''.join(chr(c) for c in buffer[prev_point:curr_point]), line])
            prev_point = curr_point
            curr_state = 0
        # deliminator
        elif curr_state == 20:
            final_lexer.append('<delim, {}>\n'.format(''.join(chr(buffer[curr_point]))))
            final_array_lexer.append(['delim', ''.join(chr(buffer[curr_point])), line])
            curr_point += 1
            prev_point = curr_point
            curr_state = 0
        # +, -
        elif curr_state == 21:
            final_lexer.append('<expr, {}>\n'.format(''.join(chr(buffer[curr_point]))))
            final_array_lexer.append(['expr', chr(buffer[curr_point]), line])
            curr_point += 1
            prev_point = curr_point
            curr_state = 0
        # /, %, *
        elif curr_state == 22:
            final_lexer.append('<term, {}>\n'.format(''.join(chr(buffer[curr_point]))))
            final_array_lexer.append(['term', ''.join(chr(buffer[curr_point])), line])
            curr_point += 1
            prev_point = curr_point
            curr_state = 0
        # panic state: double . not followed by integer
        elif curr_state == 23:
            if contBuff:
                if currBuff == 0:
                    if curr_point == 0:
                        doubleLex = buffB[cont_point:] + buffB[:-1]
                        delimLex = buffB[-1]
                    else:
                        doubleLex = buffA[cont_point:] + buffA[:curr_point-1]
                        delimLex = buffA[curr_point-1]                    
                else: 
                    if curr_point == 0:
                        doubleLex = buffA[cont_point:] + buffA[:-1]
                        delimLex = buffA[-1]
                    else:
                        doubleLex = buffA[cont_point:] + buffB[:curr_point-1]
                        delimLex = buffB[curr_point-1]
                    
                final_lexer.append('<double, {}>\n'.format(''.join(chr(c) for c in doubleLex)))
                final_array_lexer.append(['double', ''.join(chr(c) for c in doubleLex), line])
                final_lexer.append('<delim, {}>\n'.format(''.join(chr(delimLex))))
                final_array_lexer.append(['delim', ''.join(chr(delimLex))])
                contBuff = False
                cont_point = 0
            else:
                final_lexer.append('<double, {}>\n'.format(''.join(chr(c) for c in buffer[prev_point:curr_point-1])))
                final_array_lexer.append(['double', ''.join(chr(c) for c in buffer[prev_point:curr_point-1]), line])
                final_lexer.append('<delim, {}>\n'.format(''.join(chr(buffer[curr_point-1]))))
                final_array_lexer.append(['delim', ''.join(chr(buffer[curr_point-1])), line])
            prev_point = curr_point
            curr_state = 0
        # panic state: double E not followed by digit
        elif curr_state == 24:
            if contBuff:
                if currBuff == 0:
                    if curr_point == 0:
                        fullLex = buffB[cont_point:] + buffB[:-1]
                    else:
                        fullLex = buffA[cont_point:] + buffA[:curr_point-1]
                else: 
                    if curr_point == 0:
                        fullLex = buffA[cont_point:] + buffA[:-1]
                    else:
                        fullLex = buffA[cont_point:] + buffB[:curr_point-1]
                    
                final_lexer.append('<double, {}>\n'.format(''.join(chr(c) for c in fullLex)))
                final_array_lexer.append(['double', ''.join(chr(c) for c in fullLex), line])
                contBuff = False
                cont_point = 0
            else:
                final_lexer.append('<double, {}>\n'.format(''.join(chr(c) for c in buffer[prev_point:curr_point-1])))
                final_array_lexer.append(['double', ''.join(chr(c) for c in buffer[prev_point:curr_point-1]), line])
            prev_point = curr_point - 1
            curr_point -= 1
            curr_state = 0
        # \n to track lines for errors
        elif curr_state == 25:
            line += 1
            prev_point = curr_point + 1
            curr_point += 1
            curr_state = 0
        # determine if lexeme continues in next buffer
        elif curr_point + 1 == len(buffer):
            if contBuff:
                final_errors.append("error line {}: value exceeds character limit\n".format(line))
            else:
                if not (int(TRANS_TABLE[curr_state][buffer[curr_point] + 1]) == 0):
                    contBuff = True
                    cont_point = prev_point
                else: 
                    contBuff = False
                    cont_point = 0
            curr_point += 1
        # else continue reading
        else:
            curr_point += 1

'''
#* run the lexer
writes final errors and token-lexeme pairs into respective txt files
params: -
return: final_array_lexer = array of token-lexeme array pairs for parser
'''
def runLexer():
    global buffA, buffB, currBuff
    buffA = fillBuffer(code_data)
    while not buffA == -1 and not buffB == -1:
        if currBuff == 0:
            readBuffer(buffA)
            currBuff = 1
            buffB = fillBuffer(code_data)
        else: 
            readBuffer(buffB)
            currBuff = 0
            buffA = fillBuffer(code_data)

    # handle any unfinished lexemes at the end
    if contBuff:
        if currBuff == 1:
            if curr_state == 9:
                final_lexer.append('<{}, {}>\n'.format(getKeywordToken(''.join(chr(c) for c in buffA[cont_point:]), KEYWORDS), ''.join(chr(c) for c in buffA[cont_point:])))
                final_array_lexer.append([getKeywordToken(''.join(chr(c) for c in buffA[cont_point:]), KEYWORDS), ''.join(chr(c) for c in buffA[cont_point:]), line])
            elif curr_state == 11:
                final_lexer.append('<int, {}>\n'.format(''.join(chr(c) for c in buffA[cont_point:])))
                final_array_lexer.append(['int', ''.join(chr(c) for c in buffA[cont_point:]), line])
            elif curr_state == 13:
                final_lexer.append('<double, {}>\n'.format(''.join(chr(c) for c in buffA[cont_point:])))
                final_array_lexer.append(['double', ''.join(chr(c) for c in buffA[cont_point:]), line])
            elif curr_state == 14:
                final_lexer.append('<doubleE, {}>\n'.format(''.join(chr(c) for c in buffA[cont_point:])))
                final_array_lexer.append(['doubleE', ''.join(chr(c) for c in buffA[cont_point:]), line])
            elif curr_state == 16:
                final_lexer.append('<doubleE, {}>\n'.format(''.join(chr(c) for c in buffA[cont_point:])))
                final_array_lexer.append(['doubleE', ''.join(chr(c) for c in buffA[cont_point:]), line])
        else:
            if curr_state == 9:
                final_lexer.append('<{}, {}>\n'.format(getKeywordToken(''.join(chr(c) for c in buffB[cont_point:]), KEYWORDS), ''.join(chr(c) for c in buffB[cont_point:])))
                final_array_lexer.append([getKeywordToken(''.join(chr(c) for c in buffB[cont_point:]), KEYWORDS), ''.join(chr(c) for c in buffB[cont_point:]), line])
            elif curr_state == 11:
                final_lexer.append('<int, {}>\n'.format(''.join(chr(c) for c in buffB[cont_point:])))
                final_array_lexer.append(['int', ''.join(chr(c) for c in buffB[cont_point:]), line])
            elif curr_state == 13:
                final_lexer.append('<double, {}>\n'.format(''.join(chr(c) for c in buffB[cont_point:])))
                final_array_lexer.append(['double', ''.join(chr(c) for c in buffB[cont_point:]), line])
            elif curr_state == 14:
                final_lexer.append('<doubleE, {}>\n'.format(''.join(chr(c) for c in buffB[cont_point:])))
                final_array_lexer.append(['doubleE', ''.join(chr(c) for c in buffB[cont_point:]), line])
            elif curr_state == 16:
                final_lexer.append('<doubleE, {}>\n'.format(''.join(chr(c) for c in buffB[cont_point:])))
                final_array_lexer.append(['doubleE', ''.join(chr(c) for c in buffB[cont_point:]), line])

    printFinals(final_lexer, final_errors, final_array_lexer)

    # write results to respective output files
    # output file for <token, lexeme> pairs
    output_lexemes = open('files/lexemes.txt', 'w')
    output_lexemes.writelines(final_lexer)
    output_lexemes.close()

    # output file for errors
    output_errors = open('files/lex_errors.txt', 'w')
    output_errors.writelines(final_errors)
    output_errors.close()
    
    return final_array_lexer

'''
#* print <token, lexeme> pairs and error results from all 3 result arrays
params: 
- final_lexer = array of token-lexeme strings
- final_errors = array of errors
- final_array_lexer = array of token-lexeme arrays
return: -
'''
def printFinals(final_lexer, final_errors, final_array_lexer):
    print('='*10)
    print('Final Lexer')
    for lex in final_lexer:
        print(lex.strip())
    print('='*10)
    print('Final Errors')
    for error in final_errors:
        print(error.strip())
    print('='*10)
    print('Final Array Lexer')
    for lex in final_array_lexer:
        print(lex)

runLexer()