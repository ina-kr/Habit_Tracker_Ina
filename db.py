import sqlite3
import json


def get_db(name='main.db'):
    db = sqlite3.connect(name)
    create_tables(db)
    return db


def create_tables(db):
    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS habit (
        name TEXT PRIMARY KEY,
        periodicity TEXT,
        checkoffdates TEXT,
        habitbreaks TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS tracker (
        checkoffdates TEXT,
        habitbreaks TEXT,
        habitName TEXT,
        FOREIGN KEY (habitName) REFERENCES habit(name))""")

    db.commit()

###############################################################################


def add_habit(db, name, periodicity, checkoffdates, habitbreaks):
    """
    Saves new habit and its attributes in the database table 'habit'.
    :param db: initialised sqlite3 database connection
    :param name: name of the habit
    :param periodicity: periodicity of the habit
    :param checkoffdates: list of checkoff dates of the current habit streak
    :param habitbreaks: list of dates the habit was checked off the last time before a habit break
    """
    cur = db.cursor()
    json_dates = json.dumps(checkoffdates)
    json_breaks = json.dumps(habitbreaks)
    cur.execute("INSERT INTO habit VALUES (?, ?, ?, ?)", (name, periodicity, json_dates, json_breaks))
    cur.execute("INSERT INTO tracker (habitName, habitbreaks, checkoffdates) VALUES(?, ?, ?)",
                (name, json_dates, json_breaks))
    db.commit()


def update_checkoffdates(db, name, checkoffdates):
    """
    Updates checkoff dates saved in the database tables 'habit' and 'tracker'.
    :param db: initialised sqlite3 database connection
    :param name: name of the habit
    :param checkoffdates: List of all checkoff dates in the current habit streak
    """
    cur = db.cursor()
    json_dates = json.dumps(checkoffdates)
    cur.execute("UPDATE habit SET checkoffdates = ? WHERE name = ?", (json_dates, name))
    cur.execute("UPDATE tracker SET checkoffdates = ? WHERE habitName = ?", (json_dates, name))
    db.commit()


def update_habitbreaks(db, name, habitbreaks):
    """
    Updates habit breaks saved in the database table 'tracker'.
    :param db: initialised sqlite3 database connection
    :param name: name of the habit
    :param habitbreaks: List of all dates on which the habit was last checked off before the break
    """
    cur = db.cursor()
    json_breaks = json.dumps(habitbreaks)
    cur.execute("UPDATE tracker SET habitbreaks = ? WHERE habitName = ?", (json_breaks, name))
    db.commit()


def get_habit_data(db, name):
    """
    Lists all data from habit saved in the table 'habit' (name, periodicity, checkoffdates)
    :param db: initialised sqlite3 database connection
    :param name: name of the habit
    """
    cur = db.cursor()
    cur.execute("SELECT * FROM habit WHERE name=?", (name, ))
    return cur.fetchall()


def get_tracker_data(db, name):
    """
    Lists all data from habit saved in the table 'tracker' (name, checkoffdates, habitbreaks)
    :param db: initialised sqlite3 database connection
    :param name: name of the habit
    """
    cur = db.cursor()
    cur.execute("SELECT * FROM tracker WHERE habitName=?", (name, ))
    return cur.fetchall()


###############################################################################


def get_checkoffdates(db, name):
    """
    Lists all checkoff dates of the current habit streak.
    :param db: initialised sqlite3 database connection
    :param name: name of the habit
    """
    cur = db.cursor()
    cur.execute("SELECT checkoffdates FROM habit WHERE name=?", (name, ))
    return cur.fetchall()


def get_habitbreaks(db, name):
    """
    Lists all dates on which the habit was last checked off before a break.
    :param db: initialised sqlite3 database connection
    :param name: name of the habit
    """
    cur = db.cursor()
    cur.execute("SELECT habitbreaks FROM tracker WHERE habitName=?", (name, ))
    return cur.fetchall()


###############################################################################
def count_streak(db, name):
    """
    Counts the habit streak of a habit.
    The habit streak is calculated from the number of objects in the checkoff dates list.
    This list contains all dates on which the habit was checked off in the current habit streak.
    :param name: name of the habit
    :param db: initialised sqlite3 database connection
    """
    cur = db.cursor()
    habit = 'habit'
    json_data = 'checkoffdates'
    cur.execute(f"SELECT {json_data} FROM {habit} WHERE name=?", (name, ))
    result = cur.fetchall()
    anzahl_objekte = 0
    for row in result:
        json_string = row[0]
        json_data = json.loads(json_string)
        if isinstance(json_data, list):
            anzahl_objekte += len(json_data)
            return anzahl_objekte
    db.commit()


def count_breaks(db, name):
    """
    Counts the habit breaks of a habit.
    The habit breaks are calculated from the number of objects in the habit breaks list.
    This list contains all dates on which the habit was last checked off before the break.
    :param name: name of the habit
    :param db: initialised sqlite3 database connection
    """
    cur = db.cursor()
    tracker = 'tracker'
    json_breaks = 'habitbreaks'
    cur.execute(f"SELECT {json_breaks} FROM {tracker} WHERE habitName=?", (name, ))
    result = cur.fetchall()
    anzahl_objekte = 0
    for row in result:
        json_string = row[0]
        json_breaks = json.loads(json_string)
        if isinstance(json_breaks, list):
            anzahl_objekte += len(json_breaks)
            return anzahl_objekte
    db.commit()

###############################################################################


def delete_habit(db, name):
    """
    Deletes all saved habit dates from all tables (habit and tracker)
    :param name: name of the habit
    :param db: initialised sqlite3 database connection
    """
    cur = db.cursor()
    cur.execute(f"DELETE FROM habit WHERE name = ?", (name,))
    cur.execute(f"DELETE FROM tracker WHERE habitName = ?", (name,))
    db.commit()
