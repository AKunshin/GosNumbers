import random
import re


def generate_gos_numbers(amount: int) -> list:
    """Генерация списка указанного количества гос.номеров"""
    gos_numbers = []
    i = 0
    while i < amount:
        letters = ['А', 'В', 'Е', 'К', 'М', 'Н', 'О', 'Р', 'С', 'Т', 'У', 'Х']
        numbers = random.randint(1, 999)
        if numbers < 10:
            numbers = '00' + str(numbers)
        elif numbers < 100:
            numbers = '0' + str(numbers)
        gos_number = random.choice(letters) + str(numbers) + \
            random.choice(letters) + random.choice(letters)
        gos_numbers.append(gos_number)
        i += 1
    return gos_numbers


def validate_number(plate: str) -> bool:
    """Проверка гос. номера на корректность"""
    tpl = r'[АВЕКМНОРСТУХ]{1}\d{3}[АВЕКМНОРСТУХ]{2}$'
    if re.match(tpl, plate):
        return True
