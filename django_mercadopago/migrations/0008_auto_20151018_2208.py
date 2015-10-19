# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mp', '0007_preference_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='slug',
            field=models.SlugField(unique=True, help_text='El slug es usado para la URL de notificaciones de esta cuenta.', verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='created',
            field=models.DateTimeField(verbose_name='creado'),
        ),
        migrations.AlterField(
            model_name='preference',
            name='paid',
            field=models.BooleanField(verbose_name='pagado', default=False, help_text='Indica si la preferencia ha sido pagada'),
        ),
    ]
