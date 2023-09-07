import inquirer

class Prompts:
    def __init__(self) -> None:
        self.homePrompt = ["homeSelection", [
        inquirer.List('homeSelection',
                  message="Select Option",
                  choices=["Choose Game", "Settings", "Exit"],
                ),
        ]]

        self.chooseGamePrompt = ["chooseGamePrompt", [
        inquirer.List('chooseGamePrompt',
                  message="Select Game",
                  choices=["People (Longevity, Capacity and Speed)", "Back", "Exit"],
                ),
        ]]

        self.editingPrompt = ["mainEditingPrompt", [
        inquirer.List('mainEditingPrompt',
                  message="Which game would you like to edit",
                  choices=["People (Longevity, Capacity and Speed)", "Back", "Exit"],
                ),
        ]]

        self.peopleSettingsPrompt = ["peopleSettingsPrompt", [
        inquirer.List('peopleSettingsPrompt',
                  message="Select Option",
                  choices=["Add A Person", "Edit Difficulty", "Back"],
                ),
        ]]

        self.peopleDifficultyPrompt = ["peopleDifficultyPrompt", [
        inquirer.List('peopleDifficultyPrompt',
                  message="Select Difficulty",
                  choices=["Easy (5 lives and 5 streak needed)", 
                           "Normal (3 lives and usual 5 streak)", 
                           "Hard (2 Lives and new people are added faster)",
                           "One Time Only (1 life and 5 needed for a streak)",
                           "Back"],
                ),
        ]]
    

        