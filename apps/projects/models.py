import os
import uuid

from django.db import models
from django.utils.deconstruct import deconstructible


class Project(models.Model):
    """Model for the project"""
    title = models.CharField(max_length=50, null=False)
    description = models.TextField(max_length=2000, null=False)
    link = models.URLField(max_length=200, null=False)
    tags = models.ManyToManyField('Tag')


class Tag(models.Model):
    """Model for the tag object"""
    name = models.CharField(max_length=50, null=False)


class Gallery(models.Model):
    """Model for the gallery object"""
    pictures = models.ManyToManyField('Picture')


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
    image = models.ImageField(upload_to=PathAndRename('images/'),
                              height_field='height',
                              width_field='width')
