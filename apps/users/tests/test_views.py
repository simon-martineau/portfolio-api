from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from apps.users.models import User
from apps.core.utils.test.factories import UserFactory
from apps.core.utils.test import APITestCase

CREATE_USER_URL = reverse('users:register')
TOKEN_OBTAIN_URL = reverse('token_obtain_pair')
TOKEN_REFRESH_URL = reverse('token_refresh')


class PublicUserViewTests(APITestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {'email': 'test@marsimon.com', 'password': 'a;d+-394hasldf0)'}

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_create_user_exists(self):
        """Test creating user that already exists"""
        payload = {'email': 'test@marsimon.com', 'password': 'a;d+-394hasldf0)'}
        User.objects.create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_password_too_short_fails(self):
        """Test that the password must be more than 5 characters"""
        payload = {'email': 'test@marsimon.com', 'password': 'pw'}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = User.objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exists)

    def test_create_password_too_common_fails(self):
        """Test that the password must not be a common password"""
        payload = {'email': 'test@marsimon.com', 'password': 'testing123'}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = User.objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exists)

    def test_create_password_only_digits_fails(self):
        """Test that the password must not contain only digits"""
        payload = {'email': 'test@marsimon.com', 'password': '32198413216541984321654'}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = User.objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exists)

    def test_create_password_email_similar_fails(self):
        """Test that the password must not contain only digits"""
        payload = {'email': 'ihavebluehair@marsimon.com', 'password': 'ihavebluehair@marsimon'}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = User.objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exists)


class TokenViewsTests(APITestCase):
    """Test the jwt auth api"""

    def setUp(self):
        self.client = APIClient()

    def test_obtain_token_pair_for_user(self):
        """Test that a token is created for the user"""
        payload = {'email': 'test@marsimon.com', 'password': 'a;d+-394hasldf0)'}
        User.objects.create_user(**payload)

        res = self.client.post(TOKEN_OBTAIN_URL, payload)
        self.assertIn('access', res.data)
        self.assertIn('refresh', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that a token is not created if invalid credentials are given"""
        User.objects.create_user(email='test@marsimon.com', password='a;d+-394hasldf0)')
        payload = {'email': 'test@marsimon.com', 'password': 'wrongpassword'}
        res = self.client.post(TOKEN_OBTAIN_URL, payload)

        self.assertNotIn('access', res.data)
        self.assertNotIn('refresh', res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_no_user(self):
        """Test that token is not created when user does not exist"""
        payload = {'email': 'test@marsimon.com', 'password': 'a;d+-394hasldf0)'}
        res = self.client.post(TOKEN_OBTAIN_URL, payload)

        self.assertNotIn('access', res.data)
        self.assertNotIn('refresh', res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_OBTAIN_URL, {'password': 'a;d+-394hasldf0)'})

        self.assertNotIn('access', res.data)
        self.assertNotIn('refresh', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_refresh_token(self):
        """Test that refresh token works properly"""
        payload = {'email': 'test@marsimon.com', 'password': 'password123'}
        User.objects.create_user(**payload)
        res = self.client.post(TOKEN_OBTAIN_URL, payload)

        refreh_token = res.data['refresh']
        res2 = self.client.post(TOKEN_REFRESH_URL, {'refresh': refreh_token})
        self.assertIn('access', res2.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_refresh_token_invalid(self):
        """Test that refresh token returns 401 when invalid"""
        payload = {'refresh': 'some_invalid_token'}
        res = self.client.post(TOKEN_REFRESH_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('access', res.data)


# noinspection DuplicatedCode
class UserViewSetPublicTests(APITestCase):
    """Tests for the user resource endpoint from a public pov"""

    def setUp(self):
        self.client = APIClient()
        self.factory = UserFactory()
        self.base_user = self.factory.user()
        self.staff_user = self.factory.superuser()

        self.url = reverse('users:user-list')

    @staticmethod
    def _get_user_url(user: User):
        return reverse('users:user-detail', args=(user.id,))

    # Methods with public authorisation
    def test_public_list_fails_with_401(self):
        """Test that listing users fails with 401"""
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_public_delete_fails_with_404(self):
        """Test that deleting a user fails with 404"""
        url = self._get_user_url(self.base_user)
        res = self.client.delete(url)
        user_pk = self.base_user.pk
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(User.objects.filter(pk=user_pk).exists())

    def test_public_create_fails_with_401(self):
        """Test that trying to create a user returns 401"""
        payload = {'email': 'testcreateuser@marsimon.com', 'password': '9843hjf+-9834hn'}

        res = self.client.post(self.url, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(User.objects.filter(email=payload['email']).exists(), False)

    def test_plublic_update_fails_with_404(self):
        """Test that trying to update a user fails with 404"""
        payload = {'email': 'newemail@marsimon.com'}
        url = self._get_user_url(self.base_user)

        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.base_user.refresh_from_db()
        self.assertNotEqual(self.base_user.email, payload['email'])

    # Methods with private basic authorization
    def test_private_basic_user_get_fails_with_404(self):
        """Test that getting a specific user fails with 404"""
        self.client.force_authenticate(self.base_user)
        url = self._get_user_url(self.base_user)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotIn('email', res.data)

    def test_private_basic_user_list_fails_with_403(self):
        """Test that listing users fails with 403"""
        self.client.force_authenticate(self.base_user)
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_private_basic_user_delete_fails_with_404(self):
        """Test that deleting a user fails with 404"""
        self.client.force_authenticate(self.base_user)
        url = self._get_user_url(self.base_user)
        res = self.client.delete(url)
        user_pk = self.base_user.pk
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(User.objects.filter(pk=user_pk).exists())

    def test_private_basic_user_create_fails_with_403(self):
        """Test that trying to create a user returns 403"""
        self.client.force_authenticate(self.base_user)
        payload = {'email': 'testcreateuser@marsimon.com', 'password': '9843hjf+-9834hn'}

        res = self.client.post(self.url, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(User.objects.filter(email=payload['email']).exists(), False)

    def test_private_basic_user_update_fails_with_404(self):
        """Test that trying to update a user fails with 404"""
        self.client.force_authenticate(self.base_user)
        payload = {'email': 'newemail@marsimon.com'}
        url = self._get_user_url(self.base_user)

        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.base_user.refresh_from_db()
        self.assertNotEqual(self.base_user.email, payload['email'])

    # Methods with staff authorization
    def test_private_staff_user_get_succeeds(self):
        """Test that getting a specific user succeeds"""
        self.client.force_authenticate(self.staff_user)
        url = self._get_user_url(self.base_user)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertAllIn(('id', 'email'), res.data)

    def test_private_staff_user_list_succeeds(self):
        """Test that listing users succeeds"""
        self.client.force_authenticate(self.staff_user)
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertAllIn(('id', 'email', 'url', 'groups'), res.data['results'][0])

    def test_private_staff_user_delete_succeeds(self):
        """Test that deleting a user succeeds"""
        self.client.force_authenticate(self.staff_user)
        url = self._get_user_url(self.base_user)
        res = self.client.delete(url)
        user_pk = self.base_user.pk
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.filter(pk=user_pk).exists(), False)

    def test_private_staff_user_create_fails_with_405(self):
        """Test that trying to create a user returns 405"""
        self.client.force_authenticate(self.staff_user)
        payload = {'email': 'testcreateuser@marsimon.com', 'password': '9843hjf+-9834hn'}

        res = self.client.post(self.url, payload)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(User.objects.filter(email=payload['email']).exists(), False)

    def test_private_staff_user_update_succeeds(self):
        """Test that trying to update a user succeeds"""
        self.client.force_authenticate(self.staff_user)
        payload = {'email': 'newemail@marsimon.com'}
        url = self._get_user_url(self.base_user)

        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.base_user.refresh_from_db()
        self.assertEqual(self.base_user.email, payload['email'])
