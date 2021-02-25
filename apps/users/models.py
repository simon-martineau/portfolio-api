import secrets

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from apps.core.exceptions import AlreadyExistsException, IllegalCallException


class UserManager(BaseUserManager):

    def create_user(self, email: str, password: str, **extra_fields) -> 'User':
        """Creates and saves a new user"""
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email: str, password: str) -> 'User':
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


def get_default_profile_username() -> str:
    """Generates a default username"""
    while True:
        username = 'guest' + secrets.token_hex(4)
        if not Profile.objects.filter(username=username).exists():
            break
    return username


class Profile(models.Model):
    """Profile associated to each user"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=255, unique=True, default=get_default_profile_username)
    is_username_chosen = models.BooleanField(default=False)  # If the user chose their name or still use the default one

    def __str__(self):
        return f'{self.username} ({self.user.email})'

    def set_username(self, username: str) -> None:
        """Sets the username. Returns false is the username already exists"""
        if self.is_username_chosen:
            raise IllegalCallException(
                "The username cannot be changed because the field is_username_chosen is set to true")
        exists = Profile.objects.filter(username=username).exists()
        if exists:
            raise AlreadyExistsException("The username provided already exists")
        self.username = username
        self.is_username_chosen = True
        self.save(update_fields=['username', 'is_username_chosen'])
