import random


def gos_numbers_gen(amount: int) -> str:
    # Генерация гос. номера
    i = 0
    letters = ['А', 'В', 'Е', 'К', 'М', 'Н', 'О', 'Р', 'С', 'Т', 'У', 'Х']
    numbers = random.randint(1, 999)
    gos_numbers = []
    while i < amount:
        if numbers < 10:
            numbers = '00' + str(numbers)
        elif numbers < 100:
            numbers = '0' + str(numbers)

        gos_number = random.choice(letters) + str(numbers) + \
            random.choice(letters) + random.choice(letters)
        # gos_numbers = ''.join(gos_number)
        print(gos_numbers)
        i += 1
    return gos_numbers


if __name__ == "__main__":
    gos_numbers_gen(3)
