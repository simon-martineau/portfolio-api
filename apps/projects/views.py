from rest_framework import viewsets

from apps.projects.models import Tag, Project
from apps.projects.serializers import TagSerializer, ProjectSerializer, ProjectListSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset for listing and retrieving tags"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset for listing and retrieving projects"""
    queryset = Project.objects.all()
    pagination_class = None

    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectListSerializer
        return ProjectSerializer
