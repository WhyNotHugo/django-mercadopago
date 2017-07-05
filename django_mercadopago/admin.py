from django.contrib import admin, messages
from django.utils.translation import ugettext as _

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
        'paid',
    )

    def poll_status(self, request, queryset):
        payments = [payment.poll_status() for payment in queryset]
        payments_count = sum(payment is not None for payment in payments)
        messages.add_message(
            request,
            messages.SUCCESS,
            _('%d payments created.') % payments_count
        )
    poll_status.short_description = _('poll status')

    actions = (
        poll_status,
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
        'status',
        'last_update',
    )
