from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from cottages.models import Cottage
from users.models import EmailUser


class CottageModelTests(APITestCase):
    def setUp(self):
        self.user1 = EmailUser.objects.create_user(
            email='test@example.com',
            password='Test123',
            phone_number='1234567890',
            first_name='John',
            last_name='Doe'
        )
        self.user2 = EmailUser.objects.create_user(
            email='test2@example.com',
            password='Test123',
            phone_number='0123456789',
            first_name='John',
            last_name='Doe'
        )
        self.cottage1 = Cottage.objects.create(
            owner=self.user1,
            address='Test Address',
            latitude=40.7128,
            longitude=-74.0060,
            price=9500,
            options={'pool': True, 'parking': False, 'air_conditioning': True, 'wifi': False}
        )
        self.create_url = reverse("cottage-create")
        self.list_url = reverse("cottage-list")
        self.detail_url = reverse("cottage-detail", args=[self.cottage1.id])

    def test_cottage_creation(self):
        cottage_data = {
            "address": 'Test Address',
            "latitude": 40.7128,
            "longitude": -74.0060,
            "price": 9500,
            "options": {'pool': True, 'parking': False, 'air_conditioning': True, 'wifi': False}
        }
        response = self.client.post(self.create_url, cottage_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_login(self.user1)
        response = self.client.post(self.create_url, cottage_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], 'Cottage created successfully')

        cottage_data["options"]["pool"] = "hello"
        response = self.client.post(self.create_url, cottage_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("options", response.data)
        cottage_data.pop("options")
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
            "address": 'Test Address',
            "latitude": 40.3128,
            "longitude": -74.2160,
            "price": 4500,
            "options": {'pool': False, 'parking': False, 'air_conditioning': True, 'wifi': False}
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
