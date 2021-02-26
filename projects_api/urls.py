from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.projects import views as projects_views

router = DefaultRouter(trailing_slash=False)
router.register('tags', projects_views.TagViewSet)
router.register('projects', projects_views.ProjectViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('baton', include('baton.urls')),

    path('', include(router.urls)),
]
