import re

def normalize_phone(phone_number: str) -> str:
    result = re.sub(r'[^0-9]', '', phone_number)

    if result.startswith('380'):
        result = '+' + result
    else:
        result = '+38' + result

    return result