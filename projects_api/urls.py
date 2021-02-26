from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

from apps.projects import views as projects_views

router = DefaultRouter(trailing_slash=False)
router.register('tags', projects_views.TagViewSet)
router.register('projects', projects_views.ProjectViewSet)

urlpatterns = [
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),

    path('', include(router.urls)),
]
