# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mp', '0010_notification_processing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='approved',
            field=models.DateTimeField(verbose_name='aprovado', null=True),
        ),
    ]
