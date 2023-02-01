from django.test import TestCase
from plate.models import GosNumber
from plate.serializers import GosNumberSerializer


class GosNumberSerializerTestCase(TestCase):
    def test_ok(self):
        gos_number_1 = GosNumber.objects.create(number="А000АА")
        gos_number_2 = GosNumber.objects.create(number="В000ВВ")
        gs_1 = str(gos_number_1.uuid)
        gs_2 = str(gos_number_2.uuid)
        data = GosNumberSerializer([gos_number_1, gos_number_2], many=True).data
        expected_data = [
            {
                'uuid': gs_1,
                'number': "А000АА"
            },
            {
                'uuid': gs_2,
                'number': "В000ВВ"
            }
        ]
        self.assertEqual(expected_data, data)
