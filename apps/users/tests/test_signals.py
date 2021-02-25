from unittest.mock import patch
from django.test import TestCase

from apps.core.testing.factories import UserFactory


class UsersSignalsTests(TestCase):
    """Tests regarding signals in the users app"""

    def setUp(self) -> None:
        self.factory = UserFactory()

    @patch('apps.users.signals._create_user_profile')
    def test_create_user_profile_triggered_on_user_save(self, mock):
        """Test that the profile creation signal gets triggered and only at creation"""
        user = self.factory.user()
        user.save()
        self.assertTrue(mock.called)
        self.assertEqual(mock.call_count, 1)
