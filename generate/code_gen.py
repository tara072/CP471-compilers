from analyser import analyse

rootTable, program, semErr = analyse()

if semErr:
    print("Syntax errors, cannot proceed with semantic analysis.")
else:
    print("all good!")