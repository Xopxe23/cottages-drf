import datetime

from django.urls import reverse
from rest_framework import status

from core.tests_setup import APITestCaseWithSetUp


class CottageViewSetTest(APITestCaseWithSetUp):

    def setUp(self):
        super().setUp()
        self.cottage_data = {
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
            "rules": {
                "check_in_time": "12:00:00",
                "check_out_time": "12:00:00",
                "with_children": True,
                "with_pets": False,
                "smoking": False,
                "parties": True,
                "need_documents": True
            },
            "amenities": {
                "parking_spaces": 2,
                "wifi": True,
                "tv": False,
                "air_conditioner": True,
                "hair_dryer": False,
                "electric_kettle": True
            },
        }
        self.create_url = reverse("cottages-create")
        self.list_url = reverse("cottages-list")
        self.detail_url = reverse("cottages-detail", args=[self.cottage1.id])

    def test_cottage_creation(self):
        cottage_data = self.cottage_data
        response = self.client.post(self.create_url, cottage_data, format='json')
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
        cottage_data = self.cottage_data
        response = self.client.patch(self.detail_url, data=cottage_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)

        self.client.force_login(self.user1)
        response = self.client.patch(self.detail_url, data=cottage_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(cottage_data["latitude"], response.data["latitude"])

    def test_cottage_delete(self):
        self.client.force_login(self.user2)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_login(self.user1)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
