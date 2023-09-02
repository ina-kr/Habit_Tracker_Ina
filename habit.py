from db import add_habit, delete_habit, create_tables, update_checkoffdates, update_habitbreaks
from datetime import date, datetime, timedelta


class Habit:
    instances = {}

    def __init__(self, name: str, periodicity: str, checkoffdates: list[str], habitbreaks: list[str]):
        """Habit class
        :param name: the name of the habit
        :param periodicity: the periodicity of the habit
        :param checkoffdates: list of checkoff dates of the current habit streak
        :param habitbreaks: list of dates the habit was checked off the last time before a habit break
        """
        self.name = name
        self.periodicity = periodicity
        self.checkoffdates = checkoffdates.copy()
        self.habitbreaks = habitbreaks.copy()

    ############################################################################
    def store(self, db):
        """
        Saves the habit in the database.
        :param db: initialised sqlite3 database connection
        """
        create_tables(db)
        add_habit(db, self.name, self.periodicity, self.checkoffdates, self.habitbreaks)

    def append_instance(self):
        """
        Adds habit as instance to list of all instances of the Habit class.
        """
        Habit.instances[self.name] = self

    ############################################################################

    def checkoff(self, db):
        """
        Checks whether the habit was completed within the specified period or not.
        It then adds a new date to the check off list accordingly,
        or clears the data and starts a new streak with the current date.
        Adds the last date from the check off list to the habit break list before removing
        it from the check off list if a habit is broke.
        :param db: initialised sqlite3 database connection
        """
        newdate = str(date.today())
        if len(self.checkoffdates) != 0:
            format_lastcheckoff = "%Y-%m-%d"
            lastcheckoff = self.checkoffdates[-1]
            lastcheckoffdate = datetime.strptime(lastcheckoff, format_lastcheckoff)
            difference = datetime.today() - lastcheckoffdate
            if self.periodicity == 'daily':
                if difference > timedelta(days=1):
                    lastcheckoff = self.checkoffdates[-1]
                    self.habitbreaks.append(lastcheckoff)
                    self.checkoffdates = []
                    self.checkoffdates.append(newdate)
                elif difference == timedelta(days=1):
                    self.checkoffdates.append(newdate)
                else:
                    print("You already checked off your habit today")
                    self.checkoffdates.append(newdate)
            elif self.periodicity == 'weekly':
                if difference > timedelta(days=14):
                    self.checkoffdates = []
                    self.checkoffdates.append(newdate)
                    self.habitbreaks.append(newdate)
                elif timedelta(days=7) < difference < timedelta(days=14):
                    self.checkoffdates.append(newdate)
                elif difference <= timedelta(days=7):
                    print("You already checked off your habit this week")
        else:
            self.checkoffdates.append(newdate)

        self.store_checkoffdates(db)
        self.store_habitbreaks(db)

    ######################################################################
    def store_checkoffdates(self, db):
        """
        Updates list of checkoffdates of the habit in the database.
        :param db: initialised sqlite3 database connection
        """
        update_checkoffdates(db, self.name, self.checkoffdates)

    def store_habitbreaks(self, db):
        """
        Updates list of habit break dates of the habit in the database.
        :param db: initialised sqlite3 database connection
        """
        update_habitbreaks(db, self.name, self.habitbreaks)

    ######################################################################

    @classmethod
    def get_all_instances(cls):
        """
        Class method which lists all instances of Habit class
        """
        return cls.instances

    ######################################################################
    def delete_habit(self, db, name):
        """
        Deletes all data of the habit from the database.
        Deletes habit from list of all instances of the Habit class.
        :param db: initialised sqlite3 database connection
        :param name: name of the habit
        """
        delete_habit(db, name)
        del self.instances[self.name]
