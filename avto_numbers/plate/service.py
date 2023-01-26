import random
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


if __name__ == "__main__":
    gos_numbers = generate_gos_numbers()
    logger.debug(f"[INFO] Сгенерированный госномер: {gos_numbers}")
