from django.contrib import admin

from apps.projects import models


admin.site.register(models.Project)
admin.site.register(models.Tag)
admin.site.register(models.Picture)
admin.site.register(models.Gallery)
