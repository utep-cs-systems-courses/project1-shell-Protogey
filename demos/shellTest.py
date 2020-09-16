#copied from MSTeams
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

sys.ps1 = "$"
UInput = " "

while(UInput.lower() != "exit"):
    print(sys.ps1)
    UInput = input()
    #checks if the user wants to exit
    if(UInput.split(' ')[0].lower() == "exit"):
        print("Exiting\n")
        sys.exit()
    #checks if the input string is more than 2 words (command and arguement or
    #input command output)
    if(len(UInput.split()) >= 2):
        rc = os.fork()
        #Fork failed
        if rc < 0:
            print("fork failed")
            sys.exit(1)
        elif rc == 0:
            print("rc==0\n")
            first = UInput.split(' ')[0]
            second = UInput.split(' ')[1]
            #if the second word (command) is < or > 
            if(second.lower() == "<" or second.lower() == ">"):
                parse(second)
            #if the second word (command) is | (pipe)
            elif(second.lower() == "|"):
                pr, pw = os.pipe()
                for f in (pr, pw):
                    os.set_inheritable(f, True)
                args = ["wc","p3-exec.py"]

                os.close(1)
                os.dup(pw)
                for fd in (pr, pw):
                    os.close(fd)
                print("Pipe\n")
            #else unknown command inputted
            else:
                print("unknown command", UInput, "\n")
        else:
            print("WE IN THE ELSE\n")
    else:
        print("unknown command", UInput, "\n")

