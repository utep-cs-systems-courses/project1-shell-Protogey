#! /usr/bin/end python3

#WEIRD BUG FOUND, SHOWS UP DURING PIPE :(

#copied from MSTeams
def parse(cmdString):
    outFile = None
    inFile = None
    cmd = ''
    cmdString = re.sub(' +', ' ', cmdString)
    if '>' in cmdString:
        [cmd, outFile] = cmdString.split('>',1)
        outFile = outFile.strip()
    if '<' in cmdString:
        [cmd, inFile] = cmdString.split('<', 1)
        inFile = inFile.strip()
    elif outFile != None and '<' in outFile:
        [outFile, inFile] = outFile.split('<', 1)
        outFile = outFile.strip()
        inFile = inFile.strip()
    return cmd, outFile, inFile

#pipe, first and second command are extracted first from the string
def pipe(cmdString):
    first = cmdString.split('|')[0]#first pipe command
    second = cmdString.split('|')[1]#second pipe command
    #next we pipe
    pr,pw = os.pipe()
    rc = os.fork()
    if rc < 0:
        os.write(1, "fork failed".encode())
        sys.exit(1)
    elif rc == 0:                   # child (forked ok)
        os.close(1)#disconnect display (fd1)
        os.dup(pw)#pipe input to display (fd1)
        os.set_inheritable(1, True)
        for fd in (pr, pw):
            os.close(fd)#disconnect from pipe
        exe(first)#replace memory
        os.write(1, ("Could not execute: %s\n"%first).encode())
        sys.exit(1)
    else:                           # parent (forked ok)
        os.close(0)#disconnect input
        os.dup(pr)#pipe output to input (fd0)
        os.set_inheritable(0, True)
        for fd in (pr, pw):
            os.close(fd)#disconnect from pipe
        if "|" in second:#if there is more pipes, run again
            pipe(second)
        exe(second)#replace memory
        os.write(1, ("Could not execute: %s\n"%second).encode())
        sys.exit(1)
    os.write(1, "Piped..!".encode())

#exe commands, exec demo from lab
def exe(cmd):
    rc = os.fork()
    if rc<0:
        os.write(1, ("Fork failed, returning %d\n" % rc).encode())
        sys.exit(1)
    elif rc == 0:
        cmd = cmd.split()
        for dir in re.split(":", os.environ['PATH']):
            prog = "%s/%s" % (dir, cmd[0])
            try:
                os.execve(prog, cmd, os.environ)
            except FileNotFoundError:
                pass
        os.write(1, ("%s: command not found\n" % cmd[0]).encode())
    else:
        rc = os.wait()

def exeOut(cmd):
    cmd, outFile, inFile = parse(cmd)#for some reason puts command on infile, and infile at cmd
    outFile = inFile#temp hold infile
    inFile = cmd.strip()#update to infile
    cmd = outFile#update to cmd
    os.write(1, ("cmd: %s" %cmd).encode())
    os.write(1, (" outFile: %s" % outFile).encode())
    os.write(1, (" inFile: %s \n" % inFile).encode())
    cFork = os.fork()
    if cFork < 0:
        os.write(1, "Fork failed -exe".encode())
        sys.exit(1)
    elif cFork == 0:
        os.close(0) #redirect stdout
        os.open(inFile, os.O_RDONLY);#open file
        os.set_inheritable(0, True)#set inheritable
        exe(cmd)#exe c ommand
        #os.write(1, ("Could not execute: %s\n" % cmd).encode())
    else:
        cFork = os.wait()

def exeIn(cmd):
    cmd, outFile, inFile = parse(cmd)
    os.write(1, ("cmd: %s" %cmd).encode())
    os.write(1, (" outFile: %s" %outFile).encode())
    os.write(1, (" inFile: %s \n" % inFile).encode())
    cFork = os.fork()
    if cFork < 0:
        os.write(1, "Fork failed -exe".encode())
        sys.exit(1)
    elif cFork == 0:
        os.close(1) #redirect stdin
        os.open(outFile, os.O_CREAT | os.O_WRONLY);#open file
        os.set_inheritable(1, True)#set inheritable
        exe(cmd)#exe command
        #os.write(1, ("Could not execute: %s\n" % cmd).encode())
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
    #if pipe is used anywhere in the input
    if('|' in UInput):
        flag = True
        pipe(UInput)
    #if the second word (command) is < or > 
    if('<' in UInput or '>' in UInput):
        flag = True
        if('<' in UInput):
            os.write(1, "redirecting output\n".encode())
            exeOut(UInput)
        elif('>' in UInput):
            os.write(1, "redirecting input\n".encode())
            exeIn(UInput)
        else:
            os.write(1, "weird bug!".encode())    
    #else unknown command inputted
    if("cd " in UInput):
        flag = True
        os.chdir(UInput.split()[1].encode())
        os.write(1, UInput.split()[1].encode())
    if("dir" in UInput):
       flag = True
       os.write(1, (os.getcwd()+"\n").encode())
    if(flag):
        pass
    else:
        exe(UInput)
