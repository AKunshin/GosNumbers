import random
import re
from loguru import logger


def generate_gos_numbers() -> str:
    # Генерация гос. номера
    letters = ['А', 'В', 'Е', 'К', 'М', 'Н', 'О', 'Р', 'С', 'Т', 'У', 'Х']
    numbers = random.randint(1, 999)
    if numbers < 10:
        numbers = '00' + str(numbers)
    elif numbers < 100:
        numbers = '0' + str(numbers)

    gos_number = random.choice(letters) + str(numbers) + \
        random.choice(letters) + random.choice(letters)
    return gos_number


def validate_number(plate: str) -> bool:
    # Проверка гос. номера на корректность
    tpl = r'[АВЕКМНОРСТУХ]{1}\d{3}[АВЕКМНОРСТУХ]{2}$'
    if re.match(tpl, plate):
        return True
