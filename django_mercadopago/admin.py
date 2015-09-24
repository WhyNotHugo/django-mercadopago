from django.contrib import admin

from . import models


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    prepopulated_fields = {
        'slug': ('name',),
    }


admin.site.register(models.Payment)
admin.site.register(models.Preference)
admin.site.register(models.Notification)
