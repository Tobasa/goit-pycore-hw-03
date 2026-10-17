import random

MAX_VALUE: int = 1000
MIN_VALUE: int = 1


def get_numbers_ticket(_min: int, _max: int, quantity: int) -> list[int]:
    if  _min < MIN_VALUE \
        or _max > MAX_VALUE\
        or abs(_min - _max) < quantity != MAX_VALUE and _min != _max \
        or _min > _max \
        or quantity < MIN_VALUE:
        return []

    result: list[int] = random.sample(
        range(_min, _max + 1),
        k = quantity
    )
    result.sort()

    return result
