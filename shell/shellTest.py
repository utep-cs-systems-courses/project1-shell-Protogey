#! /usr/bin/end python3

#WEIRD BUG FOUND, HAVE TO WRITE EXIT TWICE AFTER PIPING

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

#pipe, first and second command are extracted first from the string
def pipe(cmdString):
    first = cmdString.split('|')[0]
    second = cmdString.split('|')[1]
    #next we pipe
    pr,pw = os.pipe()
    for f in (pr, pw):
        os.set_inheritable(f, True)
    rc = os.fork()
    if rc < 0:
        os.write(1, "fork failed".encode())
        sys.exit(1)
    elif rc == 0:                   # child (forked ok)
        stdout = os.dup(1)
        stdin = os.dup(0)
        os.close(1)#disconnect display (fd1)
        os.dup2(pw, 1)#pipe input to display (fd1)
        for fd in (pr, pw):
            os.close(fd)#disconnect from pipe
        exe(first)#replace memory
    else:                           # parent (forked ok)
        stdout = os.dup(1)
        stdin = os.dup(0)
        os.close(0)#disconnect input
        os.dup2(pr, 0)#pipe output to input (fd0)
        for fd in (pr, pw):
            os.close(fd)#disconnect from pipe
        exe(second)#replace memory

#exe commands, exec demo from lab
def exe(cmd):
    cFork = os.fork()
    if cFork < 0:
        os.write(1, "Fork failed -exe".encode())
        sys.exit(1)
    elif cFork == 0:
        cmd = cmd.split()
        for dir in re.split(":", os.environ['PATH']): # try each directory in the path
            program = "%s/%s" % (dir, cmd[0])
            try:
                os.execve(program, cmd, os.environ) # try to exec program
            except FileNotFoundError:             # ...expected
                pass                              # ...fail quietly
            os.write(2, ("Child:    Could not exec %s\n" % cmd[0]).encode())
            sys.exit(1)
    else:
        cFork = os.wait()

def exeOut(cmd):
    cFork = os.fork()
    if cFork < 0:
        os.write(1, "Fork failed -exe".encode())
        sys.exit(1)
    elif cFork == 0:
        cmd = cmd.split()
        os.close(1) #redirect stdout
        os.set_inheritable(1, True)
        for dir in re.split(":", os.environ['PATH']): # try each directory in the path
            program = "%s/%s" % (dir, cmd[0])
            try:
                os.execve(program, cmd, os.environ) # try to exec program
            except FileNotFoundError:             # ...expected
                pass                              # ...fail quietly
            os.write(2, ("Child:    Could not exec %s\n" % cmd[0]).encode())
            sys.exit(1)
    else:
        cFork = os.wait()

def exeIn(cmd):
    cFork = os.fork()
    if cFork < 0:
        os.write(1, "Fork failed -exe".encode())
        sys.exit(1)
    elif cFork == 0:
        cmd = cmd.split()
        os.close(0) #redirect stdin
        os.set_inheritable(0, True)
        for dir in re.split(":", os.environ['PATH']): # try each directory in the path
            program = "%s/%s" % (dir, cmd[0])
            try:
                os.execve(program, cmd, os.environ) # try to exec program
            except FileNotFoundError:             # ...expected
                pass                              # ...fail quietly
            os.write(2, ("Child:    Could not exec %s\n" % cmd[0]).encode())
            sys.exit(1)
    else:
        cFork = os.wait()
        
import os, sys, re

UInput = " "
directory = os.getcwd()

while(UInput != "exit"):
    if 'PS1' is os.environ:
        os.write(1, os.environ['PS1'].encode())
    else:
        os.write(1, ("$ ").encode())
    UInput = os.read(0, 100).decode() #read input, no \n
    flag = False
    #checks if the user wants to exit
    if("exit" in UInput):
        os.write(1, ("exiting\n").encode())
        sys.exit()
    #checks if the user wants to ls
    if("ls" in UInput):
        flag = True
        list = os.listdir(directory)
        for file in list:
            os.write(1, file.encode())
            os.write(1, "\n".encode())
    #checks if the user wants to see the current dir
    if("dir" in UInput):
        flag = True
        directory = os.getcwd()
        os.write(1, directory.encode())
        os.write(1, "\n".encode())
    if("pwd" in UInput):
        flag = True
        directory = os.getcwd()
        os.write(1, directory.encode())
        os.write(1, "\n".encode())
    #if pipe is used anywhere in the input
    if('|' in UInput):
        flag = True
        pipe(UInput)
    #if the second word (command) is < or > 
    if('<' in UInput or '>' in UInput):
        flag = True
        cmd, outFile, inFile = parse(UInput)
        if('<' in UInput):
            os.write(1, "redirecting output".encode())
            exeOut(UInput.split('<')[1])
        elif('>' in UInput):
            os.write(1, "redirecting input".encode())
            exeIn(UInput.split('>')[0])
        else:
            os.write(1, "weird bug!".encode())    
    #echo command
    if("echo " in UInput):
        flag = True
        os.write(1, UInput.split()[1].encode())
        os.write(1, "\n".encode())
    #else unknown command inputted
    if("cd " in UInput):
        flag = True
        os.chdir(UInput.split()[1].encode())
        os.write(1, UInput.split()[1].encode())
    if(flag):
        pass
    else:
        os.write(1, "unknown command: ".encode())
        os.write(1, UInput.split(' ')[0].encode())
        os.write(1, "\n".encode())
