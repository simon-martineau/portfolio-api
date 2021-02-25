import os
import uuid

from django.db import models
from django.utils.deconstruct import deconstructible
from colorfield.fields import ColorField


class Project(models.Model):
    """Model for the project"""
    title = models.CharField(max_length=50, null=False)
    description = models.TextField(max_length=2000, null=False)
    link = models.URLField(max_length=200, null=False)
    tags = models.ManyToManyField('Tag')
    thumbnail = models.ForeignKey('Picture', null=True, blank=True, on_delete=models.SET_NULL)
    gallery = models.ForeignKey('Gallery', null=True, blank=True, on_delete=models.SET_NULL, related_name='project')

    def __str__(self):
        return f'({self.pk}) {self.title}'


class Tag(models.Model):
    """Model for the tag object"""
    name = models.CharField(max_length=50, null=False)
    color = ColorField(default="#FFFFFF")

    def __str__(self):
        return f'({self.pk}) {self.name}'


class Gallery(models.Model):
    """Model for the gallery object"""
    pictures = models.ManyToManyField('Picture')

    def __str__(self):
        return f'{self.pk}: {self.project}'


@deconstructible
class PathAndRename:
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, _, filename):
        extension = filename.split('.')[-1]
        name = uuid.uuid4()

        filename = '{}.{}'.format(name, extension)
        return os.path.join(self.path, filename)


class Picture(models.Model):
    """Model for the picture object"""
    name = models.CharField(max_length=50, null=False)
    image = models.ImageField(upload_to=PathAndRename('images/'))
    placeholder = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f'({self.pk}) {self.name}'

