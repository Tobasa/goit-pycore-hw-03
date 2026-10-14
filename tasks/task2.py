import random

def get_numbers_ticket(_min: int, _max: int, quantity: int) -> list[int]:
    if _min < 1 or _max > 1000 or quantity < _min or quantity > _max:
        return []

    result: list[int] = random.sample(
        range(_min, _max),
        k = quantity
    )
    result.sort()

    return result
