import random
from loguru import logger


def gos_numbers_gen(amount: int) -> str:
    # Генерация гос. номера
    i = 0
    gos_numbers = []
    letters = ['А', 'В', 'Е', 'К', 'М', 'Н', 'О', 'Р', 'С', 'Т', 'У', 'Х']
    while i < amount:
        numbers = random.randint(1, 999)
        if numbers < 10:
            numbers = '00' + str(numbers)
        elif numbers < 100:
            numbers = '0' + str(numbers)

        gos_number = random.choice(letters) + str(numbers) + \
            random.choice(letters) + random.choice(letters)
        gos_numbers.append(gos_number)
        i += 1
    logger.debug(gos_numbers)
    return gos_numbers


if __name__ == "__main__":
    gos_numbers_gen(3)
