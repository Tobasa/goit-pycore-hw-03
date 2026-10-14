from datetime import datetime, date, timedelta


def get_upcoming_birthdays(users: list[dict[str, str]]) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    now: date = date.today()

    for user in users:
        users_birthday: date = datetime.strptime(user["birthday"], "%Y.%m.%d").date()
        current_year_birthday: date = date(
            year = now.year,
            month = users_birthday.month,
            day = users_birthday.day
        )

        if now <= current_year_birthday < now + timedelta(days = 7):
            if current_year_birthday.weekday() in [5, 6]:
                birthday_celebration_day = current_year_birthday + timedelta(
                    days = 1 if current_year_birthday.weekday() == 6 else 2,
                )
            else:
                birthday_celebration_day = current_year_birthday

            result.append(
                {
                    'name': user["name"],
                    'birthday': birthday_celebration_day.strftime("%Y.%m.%d"),
                }
            )

    return result
