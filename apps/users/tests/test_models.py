from django.test import TestCase

from apps.users.models import User
from apps.core.utils.test.factories import UserFactory


class UserModelTests(TestCase):

    def test_create_user_with_email_success(self):
        """Tests if user creation with email is successful"""
        email = 'test@marsimon.com'
        password = 'a;d+-394hasldf0)'

        user = User.objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_has_email_normalized(self):
        """Tests if the email for a new user is normalized"""
        email = 'Test@MARSIMON.COM'
        user = User.objects.create_user(email, 'a;d+-394hasldf0)')
        self.assertEqual(user.email, 'Test@marsimon.com')

    def test_new_user_has_permissions_mixin_attributes(self):
        """Tests if the new user has the permissions mixin attributes"""
        email = 'test@marsimon.com'
        password = 'a;d+-394hasldf0)'

        user = User.objects.create_user(
            email=email,
            password=password
        )

        self.assertTrue(hasattr(user, 'user_permissions'))


class UserManagerTests(TestCase):

    def setUp(self):
        self.usermanager = User.objects

    def test_create_new_superuser(self):
        """Tests creating a new superuser with the user manager"""
        user = self.usermanager.create_superuser(
            'test@marsimon.com',
            'a;d+-394hasldf0)'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_new_user(self):
        """Test creating a new user with the user manager"""
        user = self.usermanager.create_user(
            'test@marsimon.com',
            'a;d+-394hasldf0)'
        )
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
