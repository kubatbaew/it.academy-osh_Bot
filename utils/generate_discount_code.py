import random
import string


def generate_code():
    characters = string.ascii_uppercase + string.digits
    discount_code = ''.join(random.choice(characters) for _ in range(6))
    return discount_code
