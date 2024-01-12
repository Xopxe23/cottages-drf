from django.urls import reverse
from rest_framework import status

from core.tests_setup import APITestCaseWithSetUp
from users.models import User


class RegisterViewTest(APITestCaseWithSetUp):

    def test_register_user_and_unique_users(self):
        url = reverse('register')
        data = {
            'email': 'test12@example.com',
            'password': 'Test123',
            'phone_number': '1234567893',
            'first_name': 'John',
            'last_name': 'Doe'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(email='test@example.com')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')

        data["email"] = "test1@example.com"
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("phone_number", response.data)

        data["phone_number"] = "1234567899"
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_user_with_invalid_email_and_phone_number(self):
        url = reverse('register')
        data = {
            'email': 'test@example.com',
            'password': 'Test123',
            'phone_number': '123456789R',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            'email': 'test@example',
            'password': 'Test123',
            'phone_number': '1234567890',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginLogoutViewTest(APITestCaseWithSetUp):

    def test_login_user(self):
        url = reverse('login')
        data = {
            'email': 'test@example.com',
            'password': 'Test123',
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('success', response.data)

    def test_login_user_invalid_credentials(self):
        url = reverse('login')
        data = {
            'email': 'test@example.com',
            'password': 'WrongPassword',
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)

    def test_login_user_missing_required_field(self):
        url = reverse('login')
        data = {
            'email': 'test@example.com',
            # Missing required field 'password'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_user(self):
        url = reverse('logout')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('success', response.data)
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('success', response.data)


class UserProfileViewTest(APITestCaseWithSetUp):

    def test_get_user_profile(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('profile')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@example.com')
        self.assertEqual(response.data['first_name'], 'John')
        self.assertEqual(response.data['last_name'], 'Doe')

    def test_get_user_profile_unauthenticated(self):
        self.client.logout()
        url = reverse('profile')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", response.data)
