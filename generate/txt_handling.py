## txt handling from the lexical analysis folder - copied here for easier access
import re

# reading and saving keywords from txt file into 2d array
def read_keywords ():
    keywords = []
    file = open('files/keywords.txt', 'r')
    content=file.readlines()
    for con in content:
        res = list(filter(None, re.split(',|:|\n| ', con)))
        keywords.append(res)
    file.close()
    return keywords

# reading and saving transition table from txt file to 2d array 
def read_transition_table():
    trans_table = []
    file = open('files/transition_table.txt', 'r')
    table_content=file.readlines()
    for con in table_content:
        trans_table.append(con.split())
    file.close()
    return trans_table
