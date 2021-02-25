from unittest.mock import MagicMock, patch

from django.test import TestCase, override_settings, RequestFactory
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse
from rest_framework import status

from apps.core.middleware import HideAdminMiddleware


@override_settings(MIDDLEWARE=['apps.core.middleware.HideAdminMiddleware',
                               'django.contrib.sessions.middleware.SessionMiddleware',
                               'django.contrib.auth.middleware.AuthenticationMiddleware', ],
                   HIDE_ADMIN_ALLOWED_IPS=['123.123.123.123'])
@patch.object(HideAdminMiddleware, '__call__', side_effect=HideAdminMiddleware.__call__, autospec=True)
class HideAdminMiddlewareTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    @override_settings(HIDE_ADMIN_ALLOWED_IPS=[])
    def test_middleware_raises_error_if_allowed_ips_not_specified(self, _):
        """Test that not specifying allowed ips raises ImproperlyConfigured"""
        get_response = MagicMock()
        with self.assertRaises(ImproperlyConfigured):
            HideAdminMiddleware(get_response=get_response)

    def test_middleware_blocks_unspecified_ips_for_admin(self, mock):
        """Test that unspecified ips are blocked for admin endpoints"""
        response = self.client.get('/admin', HTTP_X_FORWARDED_FOR='222.222.222.222')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(mock.called)

    def test_middleware_allows_specified_ips_for_admin(self, mock):
        """Test that specified ips are allowed to access admin"""
        response = self.client.get('/admin/', HTTP_X_FORWARDED_FOR='123.123.123.123', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(mock.called)

    def test_middleware_allows_unspecified_for_other_than_admin(self, mock):
        """Test that the middleware does not block other urls than /admin/*"""
        response = self.client.options(reverse('api-root'), HTTP_X_FORWARDED_FOR='123.123.123.123')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(mock.called)
