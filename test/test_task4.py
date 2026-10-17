import pytest
from datetime import date, timedelta
import tasks.task4
from tasks.task4 import get_upcoming_birthdays


@pytest.fixture
def set_today(monkeypatch):
    """Fixture to mock date.today() in tasks.task4 to test arbitrary current dates."""
    def _set_today(fixed_date: date):
        class MockDate(date):
            @classmethod
            def today(cls):
                return fixed_date

        monkeypatch.setattr(tasks.task4, "date", MockDate)
        return fixed_date

    return _set_today


class TestGetUpcomingBirthdays:
    def test_empty_users_list(self) -> None:
        """Should return empty list when given an empty list of users."""
        assert get_upcoming_birthdays([]) == []

    def test_no_upcoming_birthdays(self, set_today) -> None:
        """Should return empty list when no users have birthdays in the next 7 days."""
        set_today(date(2024, 5, 10))
        users = [
            {"name": "Alice", "birthday": "1990.01.01"},
            {"name": "Bob", "birthday": "1985.05.01"},
            {"name": "Charlie", "birthday": "1992.05.20"},
            {"name": "David", "birthday": "1995.12.31"},
        ]
        assert get_upcoming_birthdays(users) == []

    def test_birthday_today_weekday(self, set_today) -> None:
        """Birthday is today on a Wednesday (weekday). Congratulation date should be today."""
        # 2024-05-15 is Wednesday (weekday 2)
        set_today(date(2024, 5, 15))
        users = [{"name": "John Doe", "birthday": "1990.05.15"}]
        result = get_upcoming_birthdays(users)
        assert result == [
            {"name": "John Doe", "congratulation_date": "2024.05.15"}
        ]

    def test_birthday_upcoming_weekday(self, set_today) -> None:
        """Birthday is within the next 7 days on a Friday."""
        # 2024-05-13 is Monday, birthday is 2024-05-17 (Friday)
        set_today(date(2024, 5, 13))
        users = [{"name": "Jane Smith", "birthday": "1988.05.17"}]
        result = get_upcoming_birthdays(users)
        assert result == [
            {"name": "Jane Smith", "congratulation_date": "2024.05.17"}
        ]

    def test_birthday_on_saturday_moved_to_monday(self, set_today) -> None:
        """Birthday falls on Saturday (weekday 5); congratulations should move +2 days to Monday."""
        # 2024-05-13 is Monday, 2024-05-18 is Saturday
        set_today(date(2024, 5, 13))
        users = [{"name": "Sat Guy", "birthday": "1995.05.18"}]
        result = get_upcoming_birthdays(users)
        # Saturday 2024.05.18 -> Monday 2024.05.20
        assert result == [
            {"name": "Sat Guy", "congratulation_date": "2024.05.20"}
        ]

    def test_birthday_on_sunday_moved_to_monday(self, set_today) -> None:
        """Birthday falls on Sunday (weekday 6); congratulations should move +1 day to Monday."""
        # 2024-05-13 is Monday, 2024-05-19 is Sunday
        set_today(date(2024, 5, 13))
        users = [{"name": "Sun Guy", "birthday": "1992.05.19"}]
        result = get_upcoming_birthdays(users)
        # Sunday 2024.05.19 -> Monday 2024.05.20
        assert result == [
            {"name": "Sun Guy", "congratulation_date": "2024.05.20"}
        ]

    def test_birthday_boundary_7_days_later_excluded(self, set_today) -> None:
        """Birthday exactly 7 days later should be excluded (now <= coming_birthday < seven_days_later)."""
        # 2024-05-10 + 7 days = 2024-05-17
        set_today(date(2024, 5, 10))
        users = [
            {"name": "Within Window", "birthday": "1990.05.16"},  # 6 days later -> included
            {"name": "Boundary Excluded", "birthday": "1990.05.17"},  # 7 days later -> excluded
        ]
        result = get_upcoming_birthdays(users)
        assert len(result) == 1
        assert result[0]["name"] == "Within Window"

    def test_birthday_already_passed_yesterday(self, set_today) -> None:
        """Birthday was yesterday; should not be included."""
        # 2024-05-10, birthday 05.09
        set_today(date(2024, 5, 10))
        users = [{"name": "Past", "birthday": "1990.05.09"}]
        assert get_upcoming_birthdays(users) == []

    def test_multiple_users_mixed(self, set_today) -> None:
        """Test multiple users with various birthdays relative to simulated 'now' date."""
        # 2026-10-12 (Monday)
        set_today(date(2026, 10, 12))
        users = [
            {"name": "Past Birthday", "birthday": "1980.10.11"},
            {"name": "Today Birthday", "birthday": "1985.10.12"},
            {"name": "Midweek Birthday", "birthday": "1990.10.15"},
            {"name": "Saturday Birthday", "birthday": "1993.10.17"},
            {"name": "Sunday Birthday", "birthday": "1995.10.18"},
            {"name": "Future Birthday", "birthday": "2000.11.01"},
        ]
        result = get_upcoming_birthdays(users)
        assert result == [
            {"name": "Today Birthday", "congratulation_date": "2026.10.12"},
            {"name": "Midweek Birthday", "congratulation_date": "2026.10.15"},
            {"name": "Saturday Birthday", "congratulation_date": "2026.10.19"},
            {"name": "Sunday Birthday", "congratulation_date": "2026.10.19"},
        ]

    def test_year_end_rollover(self, set_today) -> None:
        """Test when current date is near end of December and seven_days_later spans into next year."""
        # 2024-12-28 (Saturday), seven_days_later is 2025-01-04 (year 2025)
        set_today(date(2024, 12, 28))
        users = [
            {"name": "New Year Guy", "birthday": "1995.01.02"},  # 2025.01.02 is Thursday
        ]
        result = get_upcoming_birthdays(users)
        assert result == [
            {"name": "New Year Guy", "congratulation_date": "2025.01.02"}
        ]

    def test_leap_year_february_29_in_leap_year(self, set_today) -> None:
        """Test handling of February 29 birthday in a leap year (e.g. 2024)."""
        # 2024 is a leap year; 2024-02-25 is Sunday, 2024-02-29 is Thursday
        set_today(date(2024, 2, 25))
        users = [
            {"name": "Leap Day Guy", "birthday": "2000.02.29"},
        ]
        result = get_upcoming_birthdays(users)
        assert result == [
            {"name": "Leap Day Guy", "congratulation_date": "2024.02.29"}
        ]

    def test_february_non_leap_day_in_leap_year(self, set_today) -> None:
        """Test that regular February birthdays are not shifted/corrupted in a leap year."""
        # 2024-02-25 is Sunday; 2024-02-28 is Wednesday
        set_today(date(2024, 2, 25))
        users = [
            {"name": "Feb 28 Guy", "birthday": "1995.02.28"},
        ]
        result = get_upcoming_birthdays(users)
        assert result == [
            {"name": "Feb 28 Guy", "congratulation_date": "2024.02.28"}
        ]

    def test_leap_year_february_29_on_weekend_postponed(self, set_today) -> None:
        """Test handling of February 29 birthday when it falls on a weekend in a leap year."""
        # 2048 is a leap year; 2048-02-29 is Saturday -> postponed to Monday 2048-03-02
        set_today(date(2048, 2, 24))
        users = [
            {"name": "Leap Weekend", "birthday": "2000.02.29"},
        ]
        result = get_upcoming_birthdays(users)
        assert result == [
            {"name": "Leap Weekend", "congratulation_date": "2048.03.02"}
        ]

    def test_real_current_date(self) -> None:
        """Test with default/unmocked date.today() to ensure real environment execution works."""
        users = [
            {"name": "Far Future", "birthday": "1990.01.01"},
        ]
        result = get_upcoming_birthdays(users)
        assert isinstance(result, list)
