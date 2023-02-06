from django.test import TestCase
from plate.service import generate_gos_numbers, validate_number


class ServiceTestCase(TestCase):
    def setUp(self):
        self.number = generate_gos_numbers(amount=1)

    def test_len_gos_numbers(self):
        self.assertEqual(6, len(self.number[0]))

    def test_validate_number(self):
        testing_number = validate_number("А000АА")
        self.assertEqual(True, testing_number)

    def test_validate_generate_gos_number(self):
        result = validate_number(self.number[0])
        self.assertEqual(True, result)
