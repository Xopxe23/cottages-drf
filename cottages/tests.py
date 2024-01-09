from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from cottages.models import Cottage, CottageCategory
from towns.models import Town
from users.models import User


class CottageModelTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email='test@example.com',
            password='Test123',
            phone_number='1234567890',
            first_name='John',
            last_name='Doe'
        )
        self.user2 = User.objects.create_user(
            email='test2@example.com',
            password='Test123',
            phone_number='0123456789',
            first_name='John',
            last_name='Doe'
        )
        self.category1 = CottageCategory.objects.create(
            name="cottage",
        )
        self.town1 = Town.objects.create(
            name="Vladikavkaz"
        )
        self.cottage1 = Cottage.objects.create(
            user=self.user1,
            town=self.town1,
            category=self.category1,
            name="Family",
            description="Very good cottage",
            address='Test Address',
            latitude=40.7128,
            longitude=-74.0060,
            price=9500,
            guests=5,
            beds=4,
            rooms=3,
            total_area=50,
        )
        self.create_url = reverse("cottage-create")
        self.list_url = reverse("cottage-list")
        self.detail_url = reverse("cottage-detail", args=[self.cottage1.id])

    def test_cottage_creation(self):
        cottage_data = {
            "town": self.town1.id,
            "category": self.category1.id,
            "name": "Family",
            "description": "Very good cottage",
            "address": 'Test Address',
            "latitude": 40.7128,
            "longitude": -74.0060,
            "price": 9500,
            "guests": 5,
            "beds": 4,
            "rooms": 3,
            "total_area": 50,
        }
        response = self.client.post(self.create_url, cottage_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_login(self.user1)
        response = self.client.post(self.create_url, cottage_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        cottage_data.pop("guests")
        response = self.client.post(self.create_url, cottage_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cottage_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(response.data))

    def test_cottage_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(self.cottage1.id), response.data["id"])

    def test_cottage_update(self):
        self.client.force_login(self.user2)
        cottage_data = {
            "name": "Family",
            "description": "Very good cottage",
            "address": 'Test Address',
            "latitude": 40.7128,
            "longitude": -74.0060,
            "price": 9500,
            "guests": 5,
            "beds": 4,
            "rooms": 3,
            "total_area": 50,
        }
        response = self.client.put(self.detail_url, data=cottage_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)

        self.client.force_login(self.user1)
        response = self.client.put(self.detail_url, data=cottage_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(cottage_data["latitude"], response.data["latitude"])

    def test_cottage_delete(self):
        self.client.force_login(self.user2)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_login(self.user1)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
