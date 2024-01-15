import json
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import pytz


class Workout:
    def __init__(self, date, workoutDay, dayOfWeek):
        self.date = date
        self.workoutDay = workoutDay
        self.dayOfWeek = dayOfWeek
        self.exercises = []

    def addExercise(self, exercise):
        self.exercises.append(exercise)

    # display function displays workout, including date workout was done,
    # day of the week, the workout type, and exercises and exercise info
    def display(self):
        print(f"Date: {self.date}")
        print(f"Workout Day: {self.workoutDay}")
        print("Exercises:\n")

        for exercise in self.exercises:
            exercise.display()


class Exercise:
    def __init__(self, name, weight, sets, reps):
        self.name = name
        self.weight = float(weight)
        self.sets = int(sets)
        self.reps = reps

    # toDict used to convert an object to a dictionary
    def toDict(self):
        return {
            'name': self.name,
            'weight': self.weight,
            'sets': self.sets,
            'reps': [int(rep) for rep in self.reps],
        }

    # Display function will display the exercise's name, weight used,
    # number of sets, and reps done for each set
    def display(self):
        print(f"\t{self.name}: {self.weight} lbs")
        for i in range(self.sets):
            print(f"\t\tSet {i + 1}: {self.reps[i]} reps")

    # Function nextExercise will determine the next weight or
    # reps to be used the next time an exercise is done.
    # If the exercise is using 100 pounds for 3 sets of 8, the next
    # time the exercise is done will be used with the same weight (100 pounds)
    # but with 2 extra reps (10 reps for each sets)
    # This continues until 12 reps, where if atleast 12 reps is done for every set
    # Then the weight will increase to +5 pounds, and reps reset to 8
    def nextExercise(self):
        minReps = min(self.reps)

        if minReps < 8:
            self.reps = [8] * self.sets
        elif minReps == 8:
            self.reps = [10] * self.sets
        elif minReps == 10:
            self.reps = [12] * self.sets
        elif minReps >= 12:
            self.reps = [8] * self.sets
            self.weight = self.weight + 5
        else:
            # by defaalt function will just increase reps by 2
            self.reps = [minReps + 2] * self.sets


#  addWorkout function prompts user for workout information, such as
#  the workout day, number of exercises, name of each exercise along with the
#  weight, number of sets, and reps for each set
#
#  calls display function to display workout info for confirmation
def addWorkout():
    timeZone = pytz.timezone('US/Central')
    date = datetime.now(timeZone).strftime("%m-%d-%Y")
    todayName = datetime.now(timeZone).strftime("%A")

    if todayName == 'Monday' or todayName == 'Thursday':
        workoutDay = 'Chest and Back'

    elif todayName == 'Tuesday' or todayName == 'Friday':
        workoutDay = 'Arms'

    elif todayName == 'Wednesday' or todayName == 'Saturday':
        workoutDay = 'Legs'

    elif todayName == 'Sunday':
        print("Today is a rest day, but you may still add an excerise")
        userInputDay = input("Please enter 'Chest and Back' or 'Arms' or 'Legs' to add a workout: ")
        workoutDay = userInputDay
    else:
        print("ERROR: Problem with finding todays day, please try agian")

    print(f"\nToday is {workoutDay}.")
    workoutDayChoice = input(f"Would you like to continue with {workoutDay}? (y/n)")

    if workoutDayChoice == 'n':
        userInputDay = input("\nPlease enter 'Chest and Back' or 'Arms' or 'Legs' to add a workout: ")
        workoutDay = userInputDay
        print(f"\nToday is now {workoutDay}.")

    elif workoutDayChoice == 'y':
        print(f"\nYou have chosen to continue with {workoutDay}.")

    else:
        print("ERROR: Invalid input, please try again")

    newWorkout = Workout(date, workoutDay, todayName)

    numOfExcer = input("\nEnter the number of exercises to add: ")

    for i in range(int(numOfExcer)):
        print(f"\nExercise {i + 1}")
        print("---------")

        exerName = input("Enter the name of the exercise: ")
        weightInput = input("Enter the weight used: ")
        setsInput = input("Enter the number of sets: ")
        repsList = []
        for i in range(int(setsInput)):
            repsInput = input(f"Enter reps for set {i + 1}: ")
            repsList.append(repsInput)

        newExercise = Exercise(exerName, weightInput, setsInput, repsList)
        newWorkout.addExercise(newExercise)

    print("\nWorkout Review")
    print("--------------\n")
    newWorkout.display()
    userChoice = input("Would you like to save this workout? (y/n): ")

    if userChoice == 'y':

        try:
            with open('workoutDatabase.json', 'r') as f:
                workouts = json.load(f)

        except FileNotFoundError:
            workouts = []

        workoutDict = {
            'date': newWorkout.date,
            'workoutday': newWorkout.workoutDay,
            'Day of Week': newWorkout.dayOfWeek,
            'exercises': [exercise.toDict() for exercise in newWorkout.exercises],
        }

        workouts.append(workoutDict)

        with open("workoutDatabase.json", 'w') as f:
            json.dump(workouts, f, indent=2)

        print("\nWorkout saved!\n")
        # break

    elif userChoice == 'n':
        print("\nWorkout has not been saved, please try again.")



# printWorkout function takes a workout dictionary as input
# and prints the workout information to the console
def printWorkout(workout):
    print(f"Date: {workout['date']}")
    print(f"Workout Day: {workout['workoutday']}")
    print("Exercises:\n")

    for exercise in workout['exercises']:
        print(f"\t{exercise['name']}: {exercise['weight']} lbs")
        for i in range(len(exercise['reps'])):
            print(f"\t\tSet {i + 1}: {exercise['reps'][i]} reps")

        # print("\n")


# searchWorkout function takes a key and value input to be used
# for searching through workoutDatabase.json. The value is what to search for
# while the key represents the info in workout
def searchWorkout(key, value):
    found = False

    try:
        with open('workoutDatabase.json', 'r') as f:
            workouts = json.load(f)

        for workout in workouts:
            if workout.get(key) == value:
                found = True
                # print("\nWorkout Review")
                # print("--------------\n")
                printWorkout(workout)
                print("\n")

        if not found:
            print("ERROR: No workout found. Returning to View Previous Workout Page")

    except FileNotFoundError:
        print("\nNo file found")
        return


#  viewPreviousWorkout function will display all workouts in the workoutDatabase.json
#  Allows user to view past workouts through different means. User can find a specific
#  workout by entering the date, a type of workout by entering the workout type, or all
#  previous workouts sorted by date
def viewPrevWorkouts():
    print("\nView Previous Workouts")
    print("-----------------------")

    print("What workouts would you like to view?")
    print("(1) View Last Workout")
    print("(2) View Specific Workout")
    print("(3) View All Workouts")
    print("\n(4) Exit")
    userChoice = input("Enter your choice: ")

    if userChoice == '1':
        print("\nViewing last workout...")

        try:
            with open('workoutDatabase.json', 'r') as f:
                workouts = json.load(f)

        except FileNotFoundError:
            print("\nNo file found")
            return

        if workouts:
            lastWorkout = workouts[-1]
            print("\nPrevious Workout")
            print("----------------")
            printWorkout(lastWorkout)

        else:
            print("\nNo previous workouts found., returning to View Previous Workouts Page")


    elif userChoice == '2':
        print("\nView Specific Workout")
        print("----------------------\n")

        print("What workout would you like to view?")
        print("(1) View Workouts by Date")
        print("(2) View Workouts by Workout Day")
        print("\n(3) Exit")
        userSearchType = input("Enter your choice: ")

        if userSearchType == '1':
            workoutDate = input("Enter the date of the workout you would like to view (MM-DD-YYYY): ")

            print(f"\nWorkouts on {workoutDate}")
            print("----------------------\n")
            searchWorkout('date', workoutDate)

        elif userSearchType == '2':
            workoutDay = input("Enter the workout day you would like to view (Chest and Back, Arms, Legs): ")
            print(f"\nWorkouts on {workoutDay}")
            print("----------------------\n")

            searchWorkout('workoutday', workoutDay)

        elif userSearchType == '3':
            print("\nReturning to View Previous Workouts Page...")

        else:
            print("ERROR: Invalid input, now returning to View Previous Workouts Page...")


    elif userChoice == '3':
        print("\nViewing All Workouts...")

        try:
            with open('workoutDatabase.json', 'r') as f:
                workouts = json.load(f)

        except FileNotFoundError:
            print("\nNo file found")
            return

        if workouts:
            for workout in workouts:
                printWorkout(workout)
                print("\n")

        else:
            print("\nNo workouts found, returning to View Previous Workouts Page...")

    elif userChoice == '4':
        print("\nReturning to main menu...")

    else:
        print("ERROR: Invalid input, now returning to main menu...")

    print("\n")


# trackExercise function allows user to track a specific exercise by displaying
# a graph of the exercise date vs. the weight used. The function uses text files
# containing the names of exercises to search for
def trackExercise():
    print("\nTrack Exercise Page")
    print("--------------------")

    print("Select a workout day to find an exercise.")
    print("(1) Chest")
    print("(2) Back")
    print("(3) Biceps")
    print("(4) Triceps")
    print("(5) Shoulders")
    print("(6) Legs")
    print("\n(7) Exit")

    userChoice = input("Select an option: ")

    if userChoice == '1':
        workoutType = "Chest"

    elif userChoice == '2':
        workoutType = "Back"

    elif userChoice == '3':
        workoutType = "Biceps"

    elif userChoice == '4':
        workoutType = "Triceps"

    elif userChoice == '5':
        workoutType = "Shoulders"

    elif userChoice == '6':
        workoutType = "Legs"

    else:
        print("ERROR: Invalid input, now returning to main menu...")

    print(f"\n{workoutType} Workouts View")
    print("--------------------")

    try:
        with open(f"{workoutType}.txt", 'r') as f:
            lines = f.readlines()

        counter = 1
        for line in lines:
            print(f"({counter}) {line.strip()}")
            counter += 1

    except FileNotFoundError:
        print(f"\nERROR: File Not Found for {workoutType}, try agian.")

    # print("\n")

    exerciseChoice = input("Select an exercise to track: ")

    if 1 <= int(exerciseChoice) <= len(lines):
        exerciseToTrack = lines[int(exerciseChoice) - 1].strip()

    else:
        print("ERROR: Input out of range, please try again.")

    print(f"\nYou selected to track {exerciseToTrack}")

    print("\nNow Displaying Your Progress..")

    dates = []
    weights = []

    try:
        with open("workoutDatabase.json", 'r') as f:
            workouts = json.load(f)

        for workout in workouts:
            for exercise in workout['exercises']:
                if exercise['name'] == exerciseToTrack:
                    dates.append(workout['date'])
                    weights.append(float(exercise['weight']))

    except FileNotFoundError:
        print("\nERROR: File not found.")
        return

    print(f"Dates: {dates}")
    print(f"Weights: {weights}")

    if dates and weights:
        plt.plot(dates, weights)
        plt.xlabel('Date')
        plt.ylabel('Weight')
        plt.title(f'Weight vs Date for {exerciseToTrack}')
        plt.show()

    else:
        print("\nNo data found for the selected exercise.")


# nextWorkout function displays the next workout to be done based on tomorrows date
# The function finds the workout day associated with tomorrows date, then finds the
# most recent workout done of the same date. Then it displays the most recent workout but
# with updated weight and/or reps. The formula for calculating the next workout is within
# the nextExercise function.
def nextWorkout():
    timeZone = pytz.timezone('US/Central')

    date = datetime.now(timeZone).strftime("%m-%d-%Y")
    todayName = datetime.now(timeZone).strftime("%A")

    tomorrowDate = (datetime.now(timeZone) + timedelta(days=1)).strftime("%m-%d-%Y")
    tomorrowName = (datetime.now(timeZone) + timedelta(days=1)).strftime("%A")

    print("\nNext Workout Page")
    print("-----------------")

    if tomorrowName == 'Monday' or tomorrowName == 'Thursday':
        workoutDay = 'Chest and Back'

    elif tomorrowName == 'Tuesday' or tomorrowName == 'Friday':
        workoutDay = 'Arms'

    elif tomorrowName == 'Wednesday' or tomorrowName == 'Saturday':
        workoutDay = 'Legs'

    elif tomorrowName == 'Sunday':
        print("Tomorrow is a rest day, returning to main menu...\n")
        return

    else:
        print("ERROR: Tomorrows Date could not be found.")
        return

    # print(f"Workout for {tomorrowName} on {tomorrowDate} is {workoutDay}\n")

    try:
        with open("workoutDatabase.json", 'r') as f:
            workouts = json.load(f)

        for workout in reversed(workouts):
            if workout['workoutday'] == workoutDay:
                nextWorkout = Workout(tomorrowDate, workoutDay, tomorrowName)

                for exercises in workout['exercises']:
                    exercise = Exercise(exercises['name'], exercises['weight'], exercises['sets'], exercises['reps'])
                    exercise.nextExercise()
                    nextWorkout.addExercise(exercise)

                print(f"Workout for {tomorrowName} ({tomorrowDate}) is {workoutDay}\n")
                nextWorkout.display()
                print("\n")
                return

        print("No previous workouts found.")

    except FileNotFoundError:
        print("ERROR: File not found.")


def main():
    while True:
        print("Workout Tracker")
        print("---------------")

        print("Select an option: ")
        print("(1) Add A Workout")
        print("(2) View Previous Workouts")
        print("(3) Track Exercise Progress")
        print("(4) View Next Workout")
        print("(5) Exit")

        userChoice = input("\nEnter your choice: ")
        if userChoice == '1':
            addWorkout()
            continue

        elif userChoice == '2':
            viewPrevWorkouts()
            continue

        elif userChoice == '3':
            trackExercise()
            continue

        elif userChoice == '4':
            nextWorkout()
            continue

        elif userChoice == '5':
            exit()

        else:
            print("ERROR: Invalid option entered, try again")


main()
