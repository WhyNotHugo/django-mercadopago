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


@admin.register(models.Preference)
class PreferenceAdmin(admin.ModelAdmin):
    list_display = (
        'mp_id',
        'reference',
    )


@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'mp_id',
        'status',
        'status_detail',
        'created',
        'approved',
    )


@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'owner',
        'topic',
        'resource_id',
        'processed',
        'status',
        'last_update',
    )
