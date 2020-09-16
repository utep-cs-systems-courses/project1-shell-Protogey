def parse(cmdString):
    outFile = None
    inFile = None
    print("parse2")
    cmd = ''
    cmdString = re.sub(' +', ' ', cmdString)
    if '>' in cmdString:
        [cmd, outFile] = cmdString.split('>',1)
        outFile = outFile.strip()
    if '<' in cmd:
        [cmd, inFile] = cmd.split('<', 1)
        inFile = inFile.strip()
    elif outFile != None and '<' in outFile:
        [outFile, inFile] = outFile.split('<', 1)
        outFile = outFile.strip()
        inFile = inFile.strip()
    return cmd.split(), outFile, inFile

import os, sys, re

sys.ps1 = "user/home/"
UInput = " "

while(UInput.lower() != "exit"):
    print(sys.ps1,"\n")
    UInput = input("$")
    if(UInput.lower() == "exit"):
        print("Exiting\n")
        sys.exit()
    if(len(UInput.split()) >= 2):
        first = UInput.split(' ')[0]
        second = UInput.split(' ')[1]
        if(second.lower() == "<" or second.lower() == ">"):
            parse(second)
        elif(second.lower() == "|"):
            print("Pipe\n")
        else:
            print("unknown command", second, "\n")
    else:
        print("unknown command", UInput, "\n")

