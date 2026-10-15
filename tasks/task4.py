from datetime import datetime, date, timedelta


def get_upcoming_birthdays(users: list[dict[str, str]]) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    now: date = date.today()
    seven_days_later: date = date.today() + timedelta(days = 7)

    for user in users:
        users_birthday: date = datetime.strptime(user["birthday"], "%Y.%m.%d").date()
        coming_birthday: date = date(
            year = seven_days_later.year,
            month = users_birthday.month,
            day = users_birthday.day
        ) if users_birthday.month != 2 and users_birthday.day != 29 else date(
            # leap year case
            year=seven_days_later.year,
            month=users_birthday.month,
            day=users_birthday.day - 1
        )

        if now <= coming_birthday < seven_days_later:
            if coming_birthday.weekday() in [5, 6]:
                birthday_celebration_day = coming_birthday + timedelta(
                    days = 1 if coming_birthday.weekday() == 6 else 2,
                )
            else:
                birthday_celebration_day = coming_birthday

            result.append(
                {
                    'name': user["name"],
                    'congratulation_date': birthday_celebration_day.strftime("%Y.%m.%d"),
                }
            )

    return result
