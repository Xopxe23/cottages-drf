from django.urls import reverse
from rest_framework import status

from core.tests_setup import APITestCaseWithSetUp


class TownViewSetTest(APITestCaseWithSetUp):
    def setUp(self):
        super().setUp()
        self.town_data = {
            "name": "Заводской",
            "description": "Лучший поселок"
        }
        self.list_create_url = reverse("towns-list")
        self.detail_url = reverse("towns-detail", args=[self.town1.id,])

    def test_list_cottages(self):
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_cottages(self):
        response = self.client.post(self.list_create_url, data=self.town_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_login(self.user1)
        response = self.client.post(self.list_create_url, data=self.town_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_detail_cottages(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_cottages(self):
        self.client.force_login(self.user2)
        response = self.client.patch(self.detail_url, data={"description": "new description"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_login(self.user1)
        response = self.client.patch(self.detail_url, data={"description": "new description"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_cottages(self):
        self.client.force_login(self.user2)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_login(self.user1)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TownAttractionViewSetTest(APITestCaseWithSetUp):
    def setUp(self):
        super().setUp()
        self.attraction_data = {
            "name": "Кони",
            "description": "Осетинский и русский всадники"
        }
        self.list_create_url = reverse("attractions-list", args=[self.town1.id])
        self.detail_url = reverse("attractions-detail", args=[self.town1.id, self.attraction1.id])

    def test_list_attractions(self):
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_attractions(self):
        response = self.client.post(self.list_create_url, data=self.attraction_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_login(self.user1)
        response = self.client.post(self.list_create_url, data=self.attraction_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_detail_attractions(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_attractions(self):
        self.client.force_login(self.user2)
        response = self.client.patch(self.detail_url, data={"description": "new description"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_login(self.user1)
        response = self.client.patch(self.detail_url, data={"description": "new description"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_attractions(self):
        self.client.force_login(self.user2)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_login(self.user1)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
