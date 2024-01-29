import re

TRANS_TABLE = []
KEYWORDS = []

file = open('P1_lexical_analysis/keywords.txt', 'r')
content=file.readlines()
print(content)
for con in content:
    res = re.split(', |:|\n', con)
    # print(res)
    KEYWORDS.append(res)
file.close()

print(KEYWORDS)
print('fi' in KEYWORDS)

is_keyword = False
token = ''
i = 0
while not is_keyword and i < len(KEYWORDS):
    if 'fi' in KEYWORDS[i]:
        is_keyword = True
        token = KEYWORDS[i][0]
    else: i += 1
print(token, is_keyword)

file = open('P1_lexical_analysis/test_table.txt', 'r')
table_content=file.readlines()
for con in table_content:
    TRANS_TABLE.append(con.split())
# print(TRANS_TABLE[1])
# print(TRANS_TABLE[1][3])
file.close()


