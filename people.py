import random, time, uuid, sqlite3
import warnings
from types import SimpleNamespace
from utilities import printW, printG, printR, inputT, printStat, printCountdown
from colorama import Fore
import gspread
from prompts import Prompts
import inquirer

pt = Prompts()

warnings.filterwarnings("ignore")

class Database:
    def __init__(self):
        self.sa = gspread.service_account(filename="service_account.json")
        self.sheet = self.sa.open("SCS")
        self.worksheet = self.sheet.worksheet("MEMORY!")
        self.conn = sqlite3.connect('peopleData.db')
        self.c = self.conn.cursor()

    def addPerson(self, name, age, gender, food, occupation, colour, country):

        randomID = "0" + str(uuid.uuid4())

        self.c.execute(f"""
                    INSERT INTO people
                    (ID, name, age, gender, occupation, food, colour, country)
                    VALUES 
                    ("{randomID}", "{name}", {age}, "{gender}", "{occupation}", "{food}", "{colour}", "{country}")
                    """)
        self.conn.commit()

    def returnPersonData(self, result):
        person = SimpleNamespace(
            name=result[1],
            data=SimpleNamespace(
                age=result[2],
                gender=result[3],
                occupation=result[4],
                food=result[5],
                colour=result[6],
                country=result[7]
            )
        )

        return person

    def GetAllPeople(self, num=3):
        self.c.execute(f"""
        SELECT * FROM people
        """)

        result = self.c.fetchall()

        people = []
        for person in result:
            person = self.returnPersonData(person)
            people.append(person)

        return people

    def GetSettings(self):
        self.c.execute(f"""
        SELECT * FROM settings
        """)

        result = self.c.fetchone()

        difficulty = self.GetDifficulty(result[0])

        return difficulty

    def SetDifficulty(self, difficulty):
        self.c.execute(f"""
        UPDATE settings
        SET difficulty="{difficulty}"
        """)
        self.conn.commit()

    def GetDifficulty(self, difficulty):
        self.c.execute(f"""
        SELECT * FROM difficulties
        WHERE difficulty="{difficulty}"
        """)

        result = self.c.fetchone()

        return SimpleNamespace(
            lives=int(result[1]),
            streak=int(result[2]),
            time=int(result[3])
        )

    def GetDifficultyName(self):
        self.c.execute(f"""
        SELECT * FROM settings
        """)

        result = self.c.fetchone()
        diff = result[0]

        if diff == "oto":
            diff = "One Time Only"

        return diff

    def SubmitScore(self, score, name):
        row = 3
        empty = False
        while empty == False:
            cell = self.worksheet.get(f'A{row}')
            if len(cell) == 0:
                empty = True
                self.worksheet.update(f'A{row}', name)
                self.worksheet.update(f'B{row}', str(score))
                self.worksheet.update(f'C{row}', self.GetDifficultyName())
                self.worksheet.sort((2, 'des'), range='A3:C100')
            else:
                row += 1


class People:
    def __init__(self):
        self.data = Database()

    def Edit(self):
        while True:
            printW("Editing: People")
            answer = inquirer.prompt(pt.peopleSettingsPrompt[1])
            if answer[pt.peopleSettingsPrompt[0]] == "People (Longevity, Capacity and Speed)":
                people = People()
                people.Edit()
            if answer[pt.peopleSettingsPrompt[0]] == "Add A Person":
                self.newPersonInfo()
            elif answer[pt.peopleSettingsPrompt[0]] == "Edit Difficulty":
                self.SetDifficulty()
            else:
                return 1

    def SetDifficulty(self):
        answer = inquirer.prompt(pt.peopleDifficultyPrompt[1])
        if answer[pt.peopleDifficultyPrompt[0]] == "Easy (5 lives and 5 streak needed)":
            self.data.SetDifficulty("easy")
        elif answer[pt.peopleDifficultyPrompt[0]] == "Normal (3 lives and usual 5 streak)":
            self.data.SetDifficulty("normal")
        elif answer[pt.peopleDifficultyPrompt[0]] == "Hard (2 Lives and new people are added faster)":
            self.data.SetDifficulty("hard")
        elif answer[pt.peopleDifficultyPrompt[0]] == "One Time Only (1 life and 5 needed for a streak)":
            self.data.SetDifficulty("oto")
        else:
            return 1

    def newPersonInfo(self):
        adding = True
        while adding == True:
            name = input("Enter Name: ")
            age = int(input("Enter Age: "))
            gender = input("Enter Gender (Male or Female): ")
            occupation = input("Enter Occupation: ")
            food = input("Enter Food: ")
            colour = input("Enter Colour: ")
            country = input("Enter Country: ")

            self.data.addPerson(name, int(age), gender, food, occupation, colour, country)

            choice = input("Continue Adding? (y/n)")
            if choice == "y":
                adding = True
            else:
                adding = False

        return 1

    def Game(self):
        if self.data.GetDifficultyName() == "easy":
            self.difficulty_multiplier = 0.8
            colour = Fore.LIGHTGREEN_EX
        elif self.data.GetDifficultyName() == "normal":
            self.difficulty_multiplier = 1
            colour = Fore.LIGHTYELLOW_EX
        elif self.data.GetDifficultyName() == "hard":
            self.difficulty_multiplier = 1.5
            colour = Fore.LIGHTRED_EX
        elif self.data.GetDifficultyName() == "One Time Only":
            self.difficulty_multiplier = 2
            colour = Fore.LIGHTBLACK_EX

        print(Fore.LIGHTWHITE_EX + "Playing at Difficulty: " + colour + self.data.GetDifficultyName().upper() + f" (x{self.difficulty_multiplier} multiplier)")

        questions = ["age", "food", "occupation", "country", "colour"]

        self.lives = self.data.GetSettings().lives
        self.score = 0
        self.streak = 0

        self.people = self.data.GetAllPeople()
        self.unlockedPeople = []

        self.AddPersonInfo()

        while self.lives > 0:
            questionPrompt = questions[random.randint(0, len(questions) - 1)]

            person = self.GetRandomPerson()

            self.startTime = time.time()
            if questionPrompt == "age":
                correct = self.AgeQuestion(person)
            if questionPrompt == "food":
                correct = self.FoodQuestion(person)
            if questionPrompt == "occupation":
                correct = self.OccupationQuestion(person)
            if questionPrompt == "country":
                correct = self.CountryQuestion(person)
            if questionPrompt == "colour":
                correct = self.ColourQuestion(person)

            if correct:
                self.streak += 1
            else:
                self.streak = 0

            if self.streak > self.data.GetSettings().streak:
                if len(self.people) > 0:
                   self.AddPersonInfo()

        self.GameOver()

    def AgeQuestion(self, person):
        guess = inputT("What age is " + person.name + "? ")
        if str(person.data.age).upper() in guess.upper():
            self.endTime = time.time()
            self.CalculatePoints()
            correct = True
        else:
            self.loseLife()
            correct = False

        return correct

    def ColourQuestion(self, person):
        guess = inputT("What is the favourite colour of " + person.name + "? ")
        if str(person.data.colour).upper() in guess.upper():
            self.endTime = time.time()
            self.CalculatePoints()
            correct = True
        else:
            self.loseLife()
            correct = False

        return correct

    def FoodQuestion(self, person):
        guess = inputT("What is the favourite food of " + person.name + "? ")
        if str(person.data.food).upper() in guess.upper():
            self.endTime = time.time()
            self.CalculatePoints()
            correct = True
        else:
            self.loseLife()
            correct = False

        return correct

    def CountryQuestion(self, person):
        guess = inputT("Where is " + person.name + " from? ")
        if str(person.data.country).upper() in guess.upper():
            self.endTime = time.time()
            self.CalculatePoints()
            correct = True
        else:
            self.loseLife()
            correct = False

        return correct

    def OccupationQuestion(self, person):
        guess = inputT("What is the occupation of " + person.name + "? ")
        if str(person.data.occupation).upper() in guess.upper():
            self.endTime = time.time()
            self.CalculatePoints()
            correct = True
        else:
            self.loseLife()
            correct = False

        return correct

    def loseLife(self):
        self.lives -= 1
        if self.lives != 0:
            printR("Incorrect! Only " + str(self.lives) + " left!")
        else:
            printR("Incorrect! No Lives Left!")

    def GameOver(self):
        printR("Game Over!")
        print(Fore.LIGHTWHITE_EX + "Your score was: " + Fore.BLUE + str(self.score))

        choice = inputT("Do you want to change your score? (y/n)")
        if choice.upper() == "Y":
            name = inputT("Enter name: ")
            self.data.SubmitScore(self.score, name)
        else:
            print("Good Job!")

    def TimeBonus(self):
        elapsedTime = int(self.endTime - self.startTime)

        timeBonus = 100
        while elapsedTime > 0:
            timeBonus -= 1
            elapsedTime -= 0.25

        if timeBonus < 0:
            timeBonus = 0

        return timeBonus

    def StreakBonus(self):
        streakBonus = self.streak * 10
        return streakBonus

    def CalculatePoints(self):
        points = 10*self.difficulty_multiplier + self.TimeBonus()

        print(Fore.GREEN + "Correct!" +
              Fore.LIGHTWHITE_EX + " Gained " +
              Fore.BLUE + "10" +
              Fore.LIGHTWHITE_EX + " points! (" +
              Fore.BLUE + "+" + str(self.TimeBonus()) +
              Fore.LIGHTWHITE_EX + " speed points!)")

        if self.streak > 1:
            print(Fore.LIGHTWHITE_EX + "Gained " +
                  Fore.BLUE + str(self.StreakBonus()) +
                  Fore.LIGHTWHITE_EX + " streak points!")

        self.score += points

    def AddPersonInfo(self):
        self.streak = 0
        person = self.people[random.randint(0, len(self.people) - 1)]

        self.unlockedPeople.append(person)
        self.people.remove(person)

        printG("New Person!")
        printStat("Name", person.name)
        printStat("Age", person.data.age)
        printStat("Occupation", person.data.occupation)
        printStat("Favourite Colour", person.data.colour)
        printStat("Favourite Food", person.data.food)
        printStat("From", person.data.country)

        printCountdown(self.data.GetSettings().time)

        for i in range(0, 30):
            print("\n")

        return person

    def GetRandomPerson(self):
        person = self.unlockedPeople[random.randint(0, len(self.unlockedPeople) - 1)]
        return person
