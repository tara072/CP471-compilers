from analyser import analyse

rootTable, program, semErr = analyse()

def generate():
    if semErr:
        print("Syntax errors, cannot proceed with semantic analysis.")
        return
    
    for key, var in rootTable.functions.items():
        print('''
key: {}
{}'''.format(key, var))
    

#* MAIN
generate()