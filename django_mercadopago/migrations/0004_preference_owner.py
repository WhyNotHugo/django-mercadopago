# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mp', '0003_payment_status_detail_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='preference',
            name='owner',
            field=models.ForeignKey(to='mp.Account', verbose_name='dueño', related_name='preferences', default=1),
            preserve_default=False,
        ),
    ]
