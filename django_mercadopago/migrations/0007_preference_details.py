# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mp', '0006_preference_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='preference',
            name='price',
            field=models.DecimalField(max_digits=15, decimal_places=2, verbose_name='precio', default=-1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='preference',
            name='title',
            field=models.CharField(max_length=256, verbose_name='título', default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='preference',
            name='mp_id',
            field=models.CharField(max_length=46, help_text='El id que MercadoPago otortó a esta preferencia', verbose_name='id mercadopago'),
        ),
    ]
