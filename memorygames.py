import inquirer
import sys
from prompts import Prompts
from people import People

pt = Prompts()

def main():
    while True:
        answer = inquirer.prompt(pt.homePrompt[1])
        if answer[pt.homePrompt[0]] == "Choose Game":
            GameSelection()
        if answer[pt.homePrompt[0]] == "Settings":
            GameSettings()
        else:
            sys.exit()

def GameSelection():
    while True:
        answer = inquirer.prompt(pt.chooseGamePrompt[1])
        if answer[pt.chooseGamePrompt[0]] == "People (Longevity, Capacity and Speed)":
            people = People()
            people.Game()
        if answer[pt.chooseGamePrompt[0]] == "Back":
            return 1
        else:
            sys.exit()

def GameSettings():
    while True:
        answer = inquirer.prompt(pt.editingPrompt[1])
        if answer[pt.editingPrompt[0]] == "People (Longevity, Capacity and Speed)":
            people = People()
            people.Edit()
        if answer[pt.editingPrompt[0]] == "Back":
            return 1
        else:
            sys.exit()

main()