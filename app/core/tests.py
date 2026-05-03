from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class UserModelTests(TestCase):
    def test_create_user(self):
        user = get_user_model().objects.create_user(
            username='user',
            password='testpass123',
        )

        self.assertEqual(str(user), 'user')
        self.assertTrue(user.check_password('testpass123'))


class UserApiTests(APITestCase):
    def test_create_user(self):
        payload = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'testpass123',
        }

        response = self.client.post(reverse('register'), payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(username=payload['username'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', response.data)

    def test_create_token(self):
        get_user_model().objects.create_user(
            username='tokenuser',
            password='testpass123',
        )

        response = self.client.post(
            reverse('token_obtain_pair'),
            {'username': 'tokenuser', 'password': 'testpass123'},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_authenticated_user_can_manage_profile(self):
        user = get_user_model().objects.create_user(
            username='profileuser',
            password='testpass123',
        )
        self.client.force_authenticate(user)

        response = self.client.patch(reverse('me'), {'first_name': 'Recipe'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'Recipe')
