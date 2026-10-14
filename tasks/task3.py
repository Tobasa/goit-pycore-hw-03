import re

def normalize_phone(phone_number: str) -> str:
    result = re.sub(r'[^0-9]', '', phone_number)

    if len(result) != 12:
        result = '+38' + result
    else:
        result = '+' + result

    return result