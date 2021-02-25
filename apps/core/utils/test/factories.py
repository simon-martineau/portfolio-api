from apps.users.models import User


class UserFactory:
    user_model = User
    n_users = 0

    def _get_user_creation_params(self, params: dict) -> dict:
        defaults = {
            'email': f'testfromfactory{self.n_users}@marsimon.com',
            'password': '(-+apsodfj09832'
        }
        defaults.update(params)
        return defaults

    def user(self, **params) -> User:
        """Generates a new user"""
        params = self._get_user_creation_params(params)
        self.n_users += 1
        return self.user_model.objects.create_user(**params)

    def superuser(self, **params) -> User:
        """Generates a new user"""
        params = self._get_user_creation_params(params)
        self.n_users += 1
        return self.user_model.objects.create_superuser(**params)
