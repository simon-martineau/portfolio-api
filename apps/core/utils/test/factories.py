import random
import string

from apps.users.models import User
from apps.projects.models import Tag, Project, Picture, Gallery


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


class TagFactory:

    @staticmethod
    def _get_random_name(length=12) -> str:
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

    @staticmethod
    def _get_random_color() -> str:
        def r():
            return random.randint(0, 255)

        return '#%02X%02X%02X' % (r(), r(), r())

    def tag(self, **params) -> Tag:
        defaults = {'name': self._get_random_name(),
                    'color': self._get_random_color()}
        defaults.update(params)
        return Tag.objects.create(**defaults)


class PictureFactory:
    @staticmethod
    def _get_random_name(length=12) -> str:
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

    def picture(self, **params):
        defaults = {'name': self._get_random_name()}
        defaults.update(params)
        return Picture.objects.create(**defaults)

    def bulk_pictures(self, amount: int) -> list[Picture]:
        return Picture.objects.bulk_create((Picture(name=self._get_random_name()) for _ in range(amount)))


class GalleryFactory:
    def __init__(self):
        self._generate_pictures(10)

    def _generate_pictures(self, amount: int) -> None:
        factory = PictureFactory()
        self._pictures = factory.bulk_pictures(amount)

    def gallery(self, **params):
        gallery = Gallery.objects.create()
        amount = random.randint(1, 10)
        pictures_to_add = self._pictures[:amount]
        for picture in pictures_to_add:
            gallery.pictures.add(picture)
        return gallery


class ProjectFactory:
    TAG_AMOUNT = 3

    @staticmethod
    def _get_random_text(length=12) -> str:
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

    @staticmethod
    def _get_random_url() -> str:
        return f'https://simonmartineau.dev/{ProjectFactory._get_random_text()}'

    def _create_tags(self) -> list[Tag]:
        factory = TagFactory()
        return [factory.tag() for _ in range(self.TAG_AMOUNT)]

    def project(self, **params) -> Project:
        defaults = {
            'title': self._get_random_text(),
            'description': self._get_random_text(100),
            'link': self._get_random_url(),
            'thumbnail': PictureFactory().picture()
        }
        if 'gallery' not in defaults:
            defaults['gallery'] = GalleryFactory().gallery()

        tags = defaults.pop('tags', None)

        defaults.update(params)
        project = Project.objects.create(**defaults)

        if tags is None:
            for tag in self._create_tags():
                project.tags.add(tag)

        return project
