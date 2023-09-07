import sys
from time import sleep as s
from colorama import Fore

def printMoveT(text, delay=0, colour=Fore.LIGHTWHITE_EX):
    for char in text:
        s(delay)
        sys.stderr.write(colour + char)

def printW(text):
    print(Fore.LIGHTWHITE_EX + text)

def printG(text):
    print(Fore.LIGHTGREEN_EX + text)

def printR(text):
    print(Fore.LIGHTRED_EX + text)

def printStat(stat, value):
    print(Fore.LIGHTWHITE_EX + stat + ": " +
          Fore.CYAN + str(value))

def printCountdown(time=3):
    s(0.1)
    while time > 0:
        sys.stderr.write(str(time) + " ")
        time -= 1
        s(1)
    print("\n")

def inputT(text, colour=Fore.LIGHTWHITE_EX):
    response = input(colour + text)

    return response