# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def fake_data(apps, schema_editor):
    Account = apps.get_model('mp', 'Account')
    Notification = apps.get_model('mp', 'Notification')
    Payment = apps.get_model('mp', 'Payment')

    account = Account.objects.create(
        name="Auto-migrated",
        slug="_",
        app_id="_",
        secret_key="_",
        sandbox=True,
    )
    Notification.objects.update(owner=account)

    for payment in Payment.objects.all():
        payment.notification = Notification.objects.create(
            id=-payment.id,
            owner=account,
            topic="f",
            resource_id=str(-payment.id)
        )
        payment.save()


class Migration(migrations.Migration):

    dependencies = [
        ('mp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(verbose_name='nombre', max_length=32, help_text='Un nombre amigable para reconocer esta cuenta.')),
                ('slug', models.SlugField(verbose_name='slug', help_text='El slug es usado para la URL de notificaciones de esta cuenta.')),
                ('app_id', models.CharField(verbose_name='id de cliente', max_length=16, help_text='El APP_ID dato por MercadoPago.')),
                ('secret_key', models.CharField(verbose_name='id de cliente', max_length=32, help_text='El SECRET_KEY dado por MercadoPago.')),
                ('sandbox', models.BooleanField(default=True, verbose_name='sandbox', help_text='Indica si esta cuenta usa el modo sandbox, indicado para pruebas, en vez de transacciones reales.')),
            ],
        ),
        migrations.AddField(
            model_name='payment',
            name='notification',
            field=models.OneToOneField(related_name='payment', null=True, to='mp.Notification', help_text='La notificación que nos informó de este pago.', verbose_name='notificación'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notification',
            name='owner',
            field=models.ForeignKey(related_name='notifications', to='mp.Account', null=True, verbose_name='dueño'),
            preserve_default=False,
        ),
        migrations.RunPython(fake_data),
        migrations.AddField(
            model_name='notification',
            name='status',
            field=models.CharField(default='unp', choices=[('unp', 'Sin procesar'), ('ok', 'Okay'), ('404', 'Error 404')], max_length=3, verbose_name='estado'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='notification',
            field=models.OneToOneField(related_name='payment', default=None, to='mp.Notification', help_text='La notificación que nos informó de este pago.', verbose_name='notificación'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='notification',
            name='last_update',
            field=models.DateTimeField(auto_now=True, verbose_name='última actualización'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='processed',
            field=models.BooleanField(default=False, verbose_name='procesado'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='resource_id',
            field=models.CharField(max_length=46, verbose_name='id de recurso'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='approved',
            field=models.DateTimeField(verbose_name='aprovado'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='created',
            field=models.DateTimeField(verbose_name='fecha de creación'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='mp_id',
            field=models.IntegerField(unique=True, verbose_name='mp id'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='preference',
            field=models.ForeignKey(related_name='payments', to='mp.Preference', verbose_name='preferencia'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(max_length=16, verbose_name='estado'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='status_detail',
            field=models.CharField(max_length=16, verbose_name='detalles de estado'),
        ),
        migrations.AlterField(
            model_name='preference',
            name='payment_url',
            field=models.URLField(verbose_name='url de pagos'),
        ),
        migrations.AlterField(
            model_name='preference',
            name='reference',
            field=models.CharField(unique=True, max_length=128, verbose_name='referencia'),
        ),
        migrations.AlterField(
            model_name='preference',
            name='sandbox_url',
            field=models.URLField(verbose_name='url de sanbox'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='owner',
            field=models.ForeignKey(related_name='notifications', to='mp.Account', default=None, verbose_name='dueño'),
            preserve_default=False,
        ),
    ]
