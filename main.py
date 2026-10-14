from tasks.task1 import get_days_from_today
from tasks.task2 import get_numbers_ticket
from tasks.task3 import normalize_phone
from tasks.task4 import get_upcoming_birthdays


def main() -> None:
    # task 1
    print(get_days_from_today('2026-10-09'))
    # task 2
    print(get_numbers_ticket(1, 36, 5))
    # task 3
    raw_numbers = [
        "067\\t123 4567",
        "(095) 234-5678\\n",
        "+380 44 123 4567",
        "380501234567",
        "    +38(050)123-32-34",
        "     0503451234",
        "(050)8889900",
        "38050-111-22-22",
        "38050 111 22 11   ",
    ]

    print(
        [
            normalize_phone(phone_number)
            for phone_number in raw_numbers
        ]
    )
    # task 4
    users = [
        {"name": "John Doe", "birthday": "1985.10.15"},
        {"name": "Jane Smith", "birthday": "1990.10.17"}
    ]

    upcoming_birthdays = get_upcoming_birthdays(users)
    print(f'This week birthdays: {upcoming_birthdays}')

if __name__ == '__main__':
    main()
