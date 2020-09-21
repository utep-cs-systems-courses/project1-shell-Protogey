#! /usr/bin/end python3

#copied from MSTeams
def parse(cmdString):
    outFile = None
    inFile = None
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

def pipe(cmdString):
    #pid = os.getpid()               # get and remember pid
    pr,pw = os.pipe()
    for f in (pr, pw):
            os.set_inheritable(f, True)
    #print("pipe fds: pr=%d, pw=%d" % (pr, pw))

    import fileinput
    #print("About to fork (pid=%d)" % pid)
    rc = os.fork()
    if rc < 0:
        #print("fork failed, returning %d\n" % rc, file=sys.stderr)
        sys.exit(1)
    elif rc == 0:                   #  child - will write to pipe
        #print("Child: My pid==%d.  Parent's pid=%d" % (os.getpid(), pid), file=sys.stderr)
        args = ["wc", "p3-exec.py"]
        os.close(1)                 # redirect child's stdout
        os.dup(pw)
        for fd in (pr, pw):
            os.close(fd)
        #print("hello from child")
    else:                           # parent (forked ok)
        #print("Parent: My pid==%d.  Child's pid=%d" % (os.getpid(), rc), file=sys.stderr)
        os.close(0)
        os.dup(pr)
        for fd in (pw, pr):
            os.close(fd)
        for line in fileinput.input():
            print("From child: <%s>" % line)

import os, sys, re

UInput = " "
directory = os.getcwd()
single = False

while(UInput.lower() != "exit"):
    if 'PS1' is os.environ:
        os.write(1, os.environ['PS1'].encode())
    else:
        os.write(1, ("$ ").encode())
    UInput = input()
    #checks if the user wants to exit
    if(UInput.split(' ')[0].lower() == "exit"):
        os.write(1, ("exiting\n").encode())
        sys.exit()
    if(UInput.split(' ')[0].lower() == "ls"):
        single = True
        list = os.listdir(directory)
        for file in list:
            os.write(1, file.encode())
            os.write(1, "\n".encode())
    if(UInput.split(' ')[0].lower() == "dir"):
        single = True
        os.write(1, directory.encode())
        os.write(1, "\n".encode())
    #checks if the input string is more than 2 words (command and arguement or
    #input command output)
    if(len(UInput.split()) >= 2):
        first = UInput.split(' ')[0]
        second = UInput.split(' ')[1]
        #if the second word (command) is < or > 
        if(second.lower() == "<" or second.lower() == ">"):
            parse(UInput)
        #if the second word (command) is | (pipe)
        elif(second.lower() == "|"):
            pipe(UInput)
        #echo command
        elif(first.lower() == "echo"):
            os.write(1, second.encode())
            os.write(1, "\n".encode())
        #else unknown command inputted
        else:
            print("unknown command", UInput, "\n")
    elif(single):
        os.write(1, "\n".encode())
    else:
        print("unknown command", UInput, "\n")

