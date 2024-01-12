from django.urls import reverse
from rest_framework import status

from core.tests_setup import APITestCaseWithSetUp


class CottageReviewViewSetTest(APITestCaseWithSetUp):

    def setUp(self):
        super().setUp()
        self.list_create_url = reverse("reviews-list", args=[self.cottage1.id,])
        self.detail_url = reverse("reviews-detail", args=[self.cottage1.id, self.review1.id])
        self.review_data = {
            "cottage_rating": 4,
            "cleanliness_rating": 3,
            "owner_rating": 5,
            "comment": "Все отлично",
        }

    def test_list_reviews(self):
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_reviews(self):
        response = self.client.post(self.list_create_url, data=self.review_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_login(self.user1)
        response = self.client.post(self.list_create_url, data=self.review_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_reviews(self):
        self.client.force_login(self.user2)
        response = self.client.patch(self.detail_url, data={"owner_rating": 5}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_login(self.user1)
        response = self.client.patch(self.detail_url, data={"owner_rating": 5}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_reviews(self):
        self.client.force_login(self.user2)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_login(self.user1)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
