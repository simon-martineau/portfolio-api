from django.http import HttpRequest, Http404
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings


class HideAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        if not settings.HIDE_ADMIN_ALLOWED_IPS:
            raise ImproperlyConfigured("Setting HIDE_ADMIN_ALLOWED_IPS is not specified")
        self.allowed_ips = settings.HIDE_ADMIN_ALLOWED_IPS

    def __call__(self, request: HttpRequest):
        if request.path.startswith('/admin'):
            if not request.META.get('HTTP_X_FORWARDED_FOR') in self.allowed_ips:
                raise Http404()

        return self.get_response(request)
