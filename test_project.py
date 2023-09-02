from habit import Habit
from db import get_db, add_habit, update_checkoffdates, get_habit_data, get_checkoffdates, count_streak, count_breaks


class TestCounter:

    def setup_method(self):
        self.db = get_db("test.db")
        add_habit(self.db, "water_plants", "weekly", [], [])
        update_checkoffdates(self.db, "water_plants", ["2021-12-06"])
        update_checkoffdates(self.db, "water_plants", ["2021-12-06", "2021-12-15"])
        update_checkoffdates(self.db, "water_plants", ["2021-12-06", "2021-12-15", "2021-12-23"])

    def test_habit(self):
        meditation = Habit("Meditation", "daily", ["2023-8-01", "2023-8-02", "2023-8-03", "2023-8-04", "2023-8-05",
                                                   "2023-8-06", "2023-8-07", "2023-8-08", "2023-8-09"], [])
        not_smoke = Habit("not_smoke", "daily", ["2023-8-05", "2023-8-06", "2023-8-07", "2023-8-08"], ["2023-8-02"])
        early_to_bed = Habit("early_to_bed", "daily", ["2023-8-14", "2023-8-15", "2023-8-16", "2023-8-17", "2023-8-18"],
                          ["2023-8-05"])
        aerobic = Habit("aerobic", "weekly", ["2023-8-21", "2023-8-30"], ["2023-8-05"])

        meditation.store(self.db)
        not_smoke.store(self.db)
        early_to_bed.store(self.db)
        aerobic.store(self.db)

        meditation.append_instance()
        not_smoke.append_instance()
        early_to_bed.append_instance()
        aerobic.append_instance()

        meditation.checkoff(self.db)
        not_smoke.checkoff(self.db)
        early_to_bed.checkoff(self.db)
        aerobic.checkoff(self.db)

        meditation.delete_habit(self.db, "meditation")

    def test_db_habit(self):
        data = get_habit_data(self.db, "water_plants")
        assert len(data) == 1

        dates = get_checkoffdates(self.db, "water_plants")
        assert len(dates) == 1

        count = count_streak(self.db, "water_plants")
        assert count == 3

        count = count_breaks(self.db, "water_plants")
        assert count == 0

        instances = Habit.get_all_instances()
        assert len(instances) == 3

    def teardown_method(self):
        import os
        os.remove("test.db")
