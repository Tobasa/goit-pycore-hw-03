from datetime import datetime, date


def get_days_from_today(_date: str) -> int:
    try:
        date_as_date: date = datetime.strptime(_date, '%Y-%m-%d').date()
    except ValueError:
        raise ValueError('Date must be in format YYYY-MM-DD.')

    current_date: date = date.today()

    return (current_date - date_as_date).days
