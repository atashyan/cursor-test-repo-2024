from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('users:register')
        self.login_url = reverse('users:login')
        self.logout_url = reverse('users:logout')
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPass123!',
            'password2': 'TestPass123!'
        }

    def test_user_registration(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_user_registration_weak_password(self):
        self.user_data['password'] = 'weak'
        self.user_data['password2'] = 'weak'
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_password_mismatch(self):
        self.user_data['password2'] = 'DifferentPass123!'
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login(self):
        # Create user first
        User.objects.create_user(username='testuser', email='test@example.com', password='TestPass123!')
        
        login_data = {
            'username': 'testuser',
            'password': 'TestPass123!'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_login_invalid_credentials(self):
        login_data = {
            'username': 'nonexistent',
            'password': 'wrong'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_logout(self):
        # Create and login user
        user = User.objects.create_user(username='testuser', email='test@example.com', password='TestPass123!')
        self.client.force_authenticate(user=user)
        
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class PasswordManagementTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='OldPass123!'
        )
        self.client.force_authenticate(user=self.user)
        self.change_password_url = reverse('users:change-password')
        self.request_reset_url = reverse('users:request-password-reset')
        self.reset_password_url = reverse('users:reset-password')

    def test_change_password(self):
        data = {
            'old_password': 'OldPass123!',
            'new_password': 'NewPass123!',
            'new_password2': 'NewPass123!'
        }
        response = self.client.put(self.change_password_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify new password works
        self.assertTrue(User.objects.get(username='testuser').check_password('NewPass123!'))

    def test_change_password_wrong_old_password(self):
        data = {
            'old_password': 'WrongPass123!',
            'new_password': 'NewPass123!',
            'new_password2': 'NewPass123!'
        }
        response = self.client.put(self.change_password_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_request_password_reset(self):
        data = {'email': 'test@example.com'}
        response = self.client.post(self.request_reset_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_password(self):
        # Generate reset token
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        
        data = {
            'uid': uid,
            'token': token,
            'new_password': 'NewPass123!'
        }
        response = self.client.post(self.reset_password_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class UsernameUpdateTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )
        self.client.force_authenticate(user=self.user)
        self.update_username_url = reverse('users:update-username')

    def test_update_username(self):
        data = {
            'username': 'newusername',
            'current_password': 'TestPass123!'
        }
        response = self.client.put(self.update_username_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(id=self.user.id).username, 'newusername')

    def test_update_username_wrong_password(self):
        data = {
            'username': 'newusername',
            'current_password': 'WrongPass123!'
        }
        response = self.client.put(self.update_username_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_username_taken(self):
        # Create another user with the desired username
        User.objects.create_user(username='newusername', email='other@example.com', password='Pass123!')
        
        data = {
            'username': 'newusername',
            'current_password': 'TestPass123!'
        }
        response = self.client.put(self.update_username_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)