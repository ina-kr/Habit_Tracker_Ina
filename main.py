import questionary
from db import get_db, get_checkoffdates, count_streak, count_breaks
from habit import Habit
from analyse import show_all_habits, show_daily_habits, show_weekly_habits, get_list_breaks, get_list_streaks


def cli():
    global name
    db = get_db('main.db')
    questionary.confirm("Are you ready?").ask()

    stop = False
    while not stop:
        print("Hello, welcome to the main menu of your habit tracking app!")
        choice = questionary.select(
            "What do you want to do?",
            choices=["Show list of current habits", "Add Habit", "Check off habit",
                     "Analyse habit(s)", "Delete Habit", "Exit"]
        ).ask()

        if choice == "Show list of current habits":
            option = questionary.select(
                "Which list of current habits do you want to see?",
                choices=["All Habits", "Daily Habits", "Weekly Habits"]
            ).ask()
            if option == "All Habits":
                show_all_habits()
            elif option == "Daily Habits":
                show_daily_habits()
            elif option == "Weekly Habits":
                show_weekly_habits()

        elif choice == "Add Habit":
            name = questionary.text("Please enter the name of the habit, you want to get in!").ask()
            option = questionary.select(
                "With what periodicity do you want to execute the habit?",
                choices=["daily", "weekly"]
            ).ask()
            periodicity = option
            checkoffdates = ["2023-8-29"]
            habitbreaks = []
            habit = Habit(name, periodicity, checkoffdates, habitbreaks)
            habit.append_instance()
            habit.store(db)
            print(f"Your new habit {name} with {periodicity} periodicity has been saved!")
        elif choice == "Check off habit":
            option = questionary.select(
                "Which habit do you want to check off as done?",
                choices=list(Habit.instances.keys())
            ).ask()
            name = option
            habit = Habit.instances[option]
            habit.checkoff(db)
            print(f"You selected {option}")
            print(f"The current check off dates from {option} are: {habit.checkoffdates}")

        elif choice == "Analyse habit(s)":
            option = questionary.select(
                "What do you want to analyse?",
                choices=["Specific habit", "Compare data from all habits"]
            ).ask()

            if option == "Specific habit":
                option2 = questionary.select(
                    "Which habit do you want to analyse?",
                    choices=list(Habit.instances.keys())
                ).ask()
                name = option2
                habit = Habit.instances[option2]
                option3 = questionary.select(
                    "What do you want to analyse?",
                    choices=["Last checkoff date", "All Check-off Dates", "Habit streak",
                             "Habit breaks", "All data from habit"]).ask()
                if option3 == "Last checkoff date":
                    habit.getlastcheckoff = habit.checkoffdates[-1]
                    print(f"The last checkoffdate from your habit {name} is {habit.getlastcheckoff}.")
                elif option3 == "All Check-off Dates":
                    habit.habit_dates = get_checkoffdates(db, name)
                    print(f"The checkoff dates from your habit {name} are:")
                    print(habit.habit_dates)
                elif option3 == "Habit streak":
                    habit.count = count_streak(db, name)
                    print(f"Your current {habit.name} streak is {habit.count}")
                elif option3 == "Habit breaks":
                    habit.countbreaks = count_breaks(db, name)
                    print(f"You breaked the habit {name} {habit.countbreaks} time(s)")
                elif option3 == "All data from habit":
                    habit = Habit.instances[name]
                    habit.habit_dates = get_checkoffdates(db, name)
                    last_date = habit.checkoffdates[-1]
                    habit.count = count_streak(db, name)
                    habit.countbreaks = count_breaks(db, name)
                    if habit.periodicity == 'daily':
                        streaks = "day(s)"
                    elif habit.periodicity == 'weekly':
                        streaks = "week(s)"
                    print(f"Data for habit {name}:")
                    print(f"Periodicity: {habit.periodicity}")
                    print(f"Checkoffdates: {habit.habit_dates}")
                    print(f"Last checkoffdate: {last_date}")
                    print(f"Current streak: {habit.count} {streaks}")
                    print(f"Habit breaks: {habit.countbreaks} time(s)")
                    print(f"Dates of habit breaks: {habit.habitbreaks}")
                    print("")

            if option == "Compare data from all habits":
                option = questionary.select(
                    "What do you want to analyse?",
                    choices=["All data from all habits", "List of habit breaks of all habits",
                             "List of current habit streaks of all habits"]).ask()

                if option == "All data from all habits":
                    for name in Habit.instances.keys():
                        habit = Habit.instances[name]
                        habit.habit_dates = get_checkoffdates(db, name)
                        last_date = habit.checkoffdates[-1]
                        habit.count = count_streak(db, name)
                        habit.countbreaks = count_breaks(db, name)
                        if habit.periodicity == 'daily':
                            streaks = "day(s)"
                        elif habit.periodicity == 'weekly':
                            streaks = "week(s)"
                        print(f"Data for habit {name}:")
                        print(f"Periodicity: {habit.periodicity}")
                        print(f"Checkoffdates: {habit.habit_dates}")
                        print(f"Last checkoffdate: {last_date}")
                        print(f"Current streak: {habit.count} {streaks}")
                        print(f"Habit breaks: {habit.countbreaks} time(s)")
                        print(f"Dates of habit breaks: {habit.habitbreaks}")
                        print("The dates of habitbreaks are the dates you checked off the habit "
                              "the last time before you broke it")
                        print("")
                elif option == "List of habit breaks of all habits":
                    print("Habit breaks of all your habits sorted by decreasing frequency:")
                    list_breaks = get_list_breaks()
                    print(list_breaks)
                elif option == "List of current habit streaks of all habits":
                    print("Habit streak of all your habits sorted by decreasing frequency:")
                    get_list_streaks()

        elif choice == "Delete Habit":
            option = questionary.select(
                "Which habit do you want to delete?",
                choices=list(Habit.instances.keys())
            ).ask()
            selected_value = option
            print(f"Du hast {selected_value} ausgewählt")
            name = selected_value
            habit = Habit.instances[selected_value]
            habit.delete_habit(db, name)
            print(f"The habit {selected_value} and all associated data have been deleted.")
        else:
            print("Your're doing great!")
            print("Thank you and Goodbye, see you soon!")
            stop = True


if __name__ == '__main__':
    cli()
