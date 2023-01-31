from django.test import TestCase
from plate.service import generate_gos_numbers, validate_number
from loguru import logger


class ServiceTestCase(TestCase):
    def setUp(self):
        self.number = generate_gos_numbers()
        logger.debug(f"[TEST] test_number: {self.number}")

    def test_len_gos_numbers(self):
        self.assertEqual(6, len(self.number))

    def test_validate_number(self):
        testing_number = validate_number("А000АА")
        self.assertEqual(True, testing_number)

    def test_validate_generate_gos_number(self):
        result = validate_number(self.number)
        self.assertEqual(True, result)
