# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mp', '0002_auto_20150923_2328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='status_detail',
            field=models.CharField(
                max_length=32, verbose_name='detalles de estado'
            ),
        ),
    ]
