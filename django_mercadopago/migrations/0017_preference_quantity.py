# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mp', '0016_update_model_meta'),
    ]

    operations = [
        migrations.AddField(
            model_name='preference',
            name='quantity',
            field=models.PositiveIntegerField(
                default=1,
                verbose_name='quantity'
            ),
        ),
    ]
