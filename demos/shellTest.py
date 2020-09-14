import os, sys, re

sys.ps1 = "user/home"

UInput = " "
while(UInput != "exit"):
    print(sys.ps1,"\n")
    UInput = input("$")
    if(UInput == "exit"):
        print("Exiting\n")
    elif(UInput == "pipe"):
        print("Pipe\n")
    else:
        print("unknown command","UInput\n")
