import random
from loguru import logger


def gos_numbers_gen() -> str:
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


if __name__ == "__main__":
    gos_numbers = gos_numbers_gen(3)
    logger.debug(gos_numbers)
