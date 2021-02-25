from django.apps import AppConfig


# noinspection PyUnresolvedReferences
class UsersConfig(AppConfig):  # pragma: no cover
    name = 'apps.users'
    app_label = 'users'

    def ready(self):
        import apps.users.signals
