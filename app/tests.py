"""Test classes"""
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth.models import User


class UsersTestCase(APITestCase):
    """Users test class with user creation for an
    authenticated and not authenticated user, and
    validations"""

    def authenticate(self):
        """Method to create and authenticate user, used by
        other methods"""
        data = {"username":"ine_admin", "password":"ineadminpass"}

        user = User.objects.create_superuser('ine_admin', 'admin@ine.com', 'ineadminpass')
        user.save()

        response = self.client.post(reverse('token_obtain_pair'), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def test_create_user_not_authenticated(self):

        """This test should return a 401 Unauthorized
        http code because authorization credentials are not provided"""

        data = {"username": "johndoe",
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@ine.test",
            "password": "SuperSecurePasswd",
            "repeat_password": "SuperSecurePasswd",
            "groups": [
                "sales",
                "support",
            ]
        }

        response = self.client.post('/api/v1/users/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_user_authenticated_400(self):

        """This test should return a 400 bad request http code because password validation fails"""

        self.authenticate()

        data = {"username": "johndoe",
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@ine.test",
            "password": "SuperSecurePasswd",
            "repeat_password": "SuperSecurePasswd",
            "groups": [
                "sales",
                "support",
            ]
        }

        response = self.client.post('/api/v1/users/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_user_authenticated_201(self):

        """This test should return a 201 created http code as it passes password validation"""

        self.authenticate()

        data = {"username": "johndoe",
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@ine.test",
            "password": "AllowedPass1!",
            "repeat_password": "AllowedPass1!",
            "groups": [
                "sales",
                "support",
            ]
        }

        response = self.client.post('/api/v1/users/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
