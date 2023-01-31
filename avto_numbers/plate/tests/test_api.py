from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from loguru import logger
from plate.models import GosNumber


class GosNumberApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_username", email="test@test.com", password="pass")
        token_url = reverse("token_obtain_pair")
        self.client = APIClient()
        login_data = {"username": "test_username", "password": "pass"}
        token = self.client.post(token_url, data=login_data, format="json")
        login_token = "Bearer " + token.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=login_token)

    def test_get_jwt_token(self):
        url = reverse("token_obtain_pair")
        api_client = APIClient()
        login_data = {"username": "test_username", "password": "pass"}
        response = api_client.post(url, data=login_data, format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_generate_one(self):
        url = reverse("gosnumber-generate")
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, GosNumber.objects.all().count())

    def test_generate_many(self):
        url = reverse("gosnumber-generate")
        response = self.client.get(url, data={"amount": "3"})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(3, GosNumber.objects.all().count())

    def test_add(self):
        url = reverse("gosnumber-add")
        logger.debug(f"Path: {url}")
        data = {'plate': 'А213АА'}
        logger.debug(f"Data: {data}")
        response = self.client.post(url, data=data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, GosNumber.objects.all().count())

    # def test_generate_list(self):
    #     url = reverse("gosnumber-list")
    #     logger.debug(f"URL: {url}")
    #     self.client.force_authenticate(user=self.user)
    #     response = self.client.get(url)
    #     logger.debug(f"Response: {response.data}")
