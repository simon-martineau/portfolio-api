from django.test import TestCase
from django.urls import reverse

from apps.core.utils.test.factories import UserFactory


class AdminSiteUserTests(TestCase):

    def setUp(self):
        self.factory = UserFactory()
        self.admin_user = self.factory.superuser()
        self.client.force_login(self.admin_user)
        self.user = self.factory.user()

    def test_users_listed(self):
        """Users are listed on user page"""
        url = reverse('admin:users_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.email)

    def test_users_change_page(self):
        url = reverse('admin:users_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_users_add_page(self):
        url = reverse('admin:users_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
