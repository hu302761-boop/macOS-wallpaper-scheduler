import datetime as dt
import unittest

from wallpaper_scheduler import select_wallpaper


CONFIG = {
    "holidays": ["2026-10-01"],
    "default_wallpaper": "default",
    "rules": {
        "workday": [
            {"start": "10:00", "end": "18:00", "wallpaper": "work"},
            {"start": "18:00", "end": "19:00", "wallpaper": "transition"},
            {"start": "19:00", "end": "10:00", "wallpaper": "rest"},
        ],
        "restday": [{"start": "00:00", "end": "24:00", "wallpaper": "weekend"}],
        "holiday": [{"start": "00:00", "end": "24:00", "wallpaper": "holiday"}],
    },
}


class SchedulerTests(unittest.TestCase):
    def test_workday_and_cross_midnight(self):
        self.assertEqual(select_wallpaper(CONFIG, dt.datetime(2026, 9, 30, 11)), ("work", "workday"))
        self.assertEqual(select_wallpaper(CONFIG, dt.datetime(2026, 9, 30, 23)), ("rest", "workday"))
        self.assertEqual(select_wallpaper(CONFIG, dt.datetime(2026, 10, 1, 9)), ("holiday", "holiday"))

    def test_weekend(self):
        self.assertEqual(select_wallpaper(CONFIG, dt.datetime(2026, 9, 26, 12)), ("weekend", "restday"))


if __name__ == "__main__":
    unittest.main()
