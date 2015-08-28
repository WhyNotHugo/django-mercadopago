from django.contrib import admin

from . import models

admin.site.register(models.Payment)
admin.site.register(models.Preference)
admin.site.register(models.Notification)
