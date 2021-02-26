from rest_framework import serializers

from apps.projects import models


class TagSerializer(serializers.ModelSerializer):
    """Serializer for the tag models"""

    class Meta:
        model = models.Tag
        fields = '__all__'


class PictureSerializer(serializers.ModelSerializer):
    """Serializer for the tag models"""

    class Meta:
        model = models.Picture
        fields = '__all__'


class GallerySerializer(serializers.ModelSerializer):
    """Serializer for the tag model"""

    class Meta:
        model = models.Gallery
        fields = ('id', 'pictures',)


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for the project model"""

    class Meta:
        model = models.Project
        fields = ('id', 'title', 'description', 'link', 'tags', 'thumbnail', 'gallery')
        depth = 2


class ProjectListSerializer(serializers.ModelSerializer):
    """Serializer for the project model in list format (more shallow)"""
    href = serializers.HyperlinkedIdentityField(view_name='project-detail')

    class Meta:
        model = models.Project
        fields = ('id', 'href', 'title', 'description', 'link', 'tags', 'thumbnail')
        depth = 1

