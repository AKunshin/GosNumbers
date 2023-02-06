from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from plate.models import GosNumber
from plate.serializers import GosNumberSerializer


class GosNumberApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_username",
            email="test@test.com",
            password="pass"
        )
        token_url = reverse("token_obtain_pair")
        self.client = APIClient()
        login_data = {
            "username": "test_username",
            "password": "pass"
        }
        token = self.client.post(
            token_url,
            data=login_data,
            format="json"
        )
        login_token = "Bearer " + token.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=login_token)

    def test_get_jwt_token(self):
        url = reverse("token_obtain_pair")
        api_client = APIClient()
        login_data = {
            "username": "test_username",
            "password": "pass"
        }
        response = api_client.post(
            url,
            data=login_data,
            format="json"
        )
        if response.data["access"]:
            jwt_access = True
        self.assertEqual(jwt_access, True)
        if response.data["refresh"]:
            jwt_refresh = True
        self.assertEqual(jwt_refresh, True)

    def test_generate_one(self):
        url = reverse("gosnumber-generate")
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, GosNumber.objects.all().count())

    def test_generate_many(self):
        url = reverse("gosnumber-generate")
        response = self.client.get(url, data={"amount": "10"})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(10, GosNumber.objects.all().count())

    def test_add(self):
        url = reverse("gosnumber-add")
        data = {"plate": "А213АА"}
        response = self.client.post(url, data=data)
        gos_number_1 = GosNumber.objects.get(pk=1)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, GosNumber.objects.all().count())
        self.assertEqual(
            GosNumberSerializer(gos_number_1, many=False).data,
            response.data
        )
        response = self.client.post(url, data={})
        self.assertEqual("Не передан гос. номер", response.data["detail"])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        response = self.client.post(url, data={"plate": "S123DD"})
        self.assertEqual("Ошибка в гос. номере", response.data["detail"])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        GosNumber.objects.create(number="А001АА")
        data = {"plate": "А001АА"}
        response = self.client.post(url, data=data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual("Данный гос. номер уже содержится в БД",
                         response.data["detail"])

    def test_get_by_uuid(self):
        url = reverse("gosnumber-get")
        gos_number = GosNumber.objects.create(number="А000АА")
        gs = str(gos_number.uuid)
        response = self.client.get(url)
        self.assertEqual("Не передан uuid", response.data["detail"])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        response = self.client.get(url, data={"id": "23"})
        self.assertEqual("Неверный uuid", response.data["detail"])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        response = self.client.get(url, data={"id": gs})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
