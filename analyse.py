from habit import Habit


def get_list_breaks():
    """
    Lists the habit breaks of all habits sorted by decreasing frequency.
    The habit breaks are calculated from the number of objects in the habit breaks list.
    This list contains all the dates on which the habit was last checked off before the break.
    """
    all_instances = Habit.get_all_instances()
    sorted_breaks = sorted(all_instances.values(), key=lambda instance: len(instance.habitbreaks), reverse=True)
    for instances in sorted_breaks:
        print(instances.name, len(instances.habitbreaks))


def get_list_streaks():
    """
    Lists the current habit streak of either all habits, daily habits or weekly habits sorted by decreasing frequency.
    The habit streak is calculated from the number of objects in the checkoff dates list.
    """
    all_instances = Habit.get_all_instances()
    sorted_streaks = sorted(all_instances.values(), key=lambda instance: len(instance.checkoffdates), reverse=True)
    for instances in sorted_streaks:
        if instances.periodicity == 'daily':
            period = "day(s)"
            print(f"{instances.name}: {len(instances.checkoffdates)} {period}")
        elif instances.periodicity == 'weekly':
            period = "week(s)"
            print(f"{instances.name}: {len(instances.checkoffdates)} {period}")


def show_all_habits():
    """
    Lists all current saved habits and their periodicity.
    """
    all_instances = Habit.get_all_instances()
    for name, instances in all_instances.items():
        print(f"habit: {instances.name}, periodicity: {instances.periodicity}")


def show_daily_habits():
    """
    Lists all current daily habits.
    """
    all_instances = Habit.get_all_instances()
    for name, instances in all_instances.items():
        if instances.periodicity == 'daily':
            print(f"habit: {instances.name}, periodicity: {instances.periodicity}")


def show_weekly_habits():
    """
    Lists all current weekly habits.
    """
    all_instances = Habit.get_all_instances()
    for name, instances in all_instances.items():
        if instances.periodicity == 'weekly':
            print(f"habit: {instances.name}, periodicity: {instances.periodicity}")
