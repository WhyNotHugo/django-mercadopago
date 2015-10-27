# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mp', '0009_payment_notification_null'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='processed',
        ),
        migrations.AlterField(
            model_name='notification',
            name='status',
            field=models.CharField(choices=[('unp', 'Sin procesar'), ('pro', 'Processed'), ('old', 'With updates'), ('ign', 'Ignored'), ('ok', 'Okay'), ('404', 'Error 404'), ('err', 'Error')], default='unp', max_length=3, verbose_name='estado'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='preference',
            field=models.ForeignKey(to='mp.Preference', related_name='payments', verbose_name='preferencia', null=True),
        ),
    ]
