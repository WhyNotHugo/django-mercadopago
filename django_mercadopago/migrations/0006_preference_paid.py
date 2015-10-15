# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mp', '0005_auto_20151009_1836'),
    ]

    operations = [
        migrations.AddField(
            model_name='preference',
            name='paid',
            field=models.BooleanField(help_text='Indica si la preferencia ha sido pagada', default=False, verbose_name='Pagado'),
        ),
    ]
