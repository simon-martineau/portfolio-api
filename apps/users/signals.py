from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.users.models import User, Profile


def _create_user_profile(instance: User):
    Profile.objects.create(user=instance)
    instance.profile.save()


# https://stackoverflow.com/questions/13112302/how-do-i-mock-a-django-signal-handler
@receiver(post_save, sender=User)
def user_post_save_signal_handler(sender, instance, created, **kwargs):
    if created:
        _create_user_profile(instance)
