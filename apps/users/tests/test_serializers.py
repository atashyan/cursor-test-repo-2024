from django.test import TestCase
from django.contrib.auth import get_user_model
from ..serializers import (
    UserSerializer,
    RegisterSerializer,
    ChangePasswordSerializer,
    UpdateUsernameSerializer
)

User = get_user_model()

class UserSerializerTests(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'bio': 'Test bio',
            'birth_date': '1990-01-01'
        }
        self.user = User.objects.create_user(
            username=self.user_data['username'],
            email=self.user_data['email'],
            password='TestPass123!'
        )
        self.serializer = UserSerializer(instance=self.user)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(
            data.keys(),
            ['id', 'username', 'email', 'first_name', 'last_name', 'bio', 'birth_date', 'avatar']
        )

    def test_email_field_validation(self):
        # Test invalid email format
        invalid_email_data = self.user_data.copy()
        invalid_email_data['email'] = 'invalid-email'
        serializer = UserSerializer(data=invalid_email_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

        # Test duplicate email
        User.objects.create_user(username='another', email='another@example.com', password='Pass123!')
        duplicate_email_data = self.user_data.copy()
        duplicate_email_data['email'] = 'another@example.com'
        serializer = UserSerializer(data=duplicate_email_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

class RegisterSerializerTests(TestCase):
    def setUp(self):
        self.valid_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'StrongPass123!',
            'password2': 'StrongPass123!',
            'first_name': 'New',
            'last_name': 'User'
        }

    def test_valid_registration(self):
        serializer = RegisterSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, self.valid_data['username'])
        self.assertEqual(user.email, self.valid_data['email'])

    def test_password_mismatch(self):
        invalid_data = self.valid_data.copy()
        invalid_data['password2'] = 'DifferentPass123!'
        serializer = RegisterSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    def test_weak_password(self):
        invalid_data = self.valid_data.copy()
        invalid_data['password'] = 'weak'
        invalid_data['password2'] = 'weak'
        serializer = RegisterSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    def test_duplicate_email(self):
        # Create a user first
        User.objects.create_user(username='existing', email=self.valid_data['email'], password='Pass123!')
        serializer = RegisterSerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

class ChangePasswordSerializerTests(TestCase):
    def setUp(self):
        self.valid_data = {
            'old_password': 'OldPass123!',
            'new_password': 'NewPass123!',
            'new_password2': 'NewPass123!'
        }

    def test_passwords_match(self):
        serializer = ChangePasswordSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_passwords_mismatch(self):
        invalid_data = self.valid_data.copy()
        invalid_data['new_password2'] = 'DifferentPass123!'
        serializer = ChangePasswordSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('new_password', serializer.errors)

    def test_weak_new_password(self):
        invalid_data = self.valid_data.copy()
        invalid_data['new_password'] = 'weak'
        invalid_data['new_password2'] = 'weak'
        serializer = ChangePasswordSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('new_password', serializer.errors)

class UpdateUsernameSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='oldusername',
            email='test@example.com',
            password='TestPass123!'
        )
        self.valid_data = {
            'username': 'newusername',
            'current_password': 'TestPass123!'
        }
        self.context = {'request': type('Request', (), {'user': self.user})}

    def test_valid_username_update(self):
        serializer = UpdateUsernameSerializer(
            instance=self.user,
            data=self.valid_data,
            context=self.context
        )
        self.assertTrue(serializer.is_valid())

    def test_incorrect_password(self):
        invalid_data = self.valid_data.copy()
        invalid_data['current_password'] = 'WrongPass123!'
        serializer = UpdateUsernameSerializer(
            instance=self.user,
            data=invalid_data,
            context=self.context
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn('current_password', serializer.errors)

    def test_duplicate_username(self):
        # Create another user with the desired username
        User.objects.create_user(
            username=self.valid_data['username'],
            email='another@example.com',
            password='Pass123!'
        )
        serializer = UpdateUsernameSerializer(
            instance=self.user,
            data=self.valid_data,
            context=self.context
        )
        self.assertFalse(serializer.is_valid())