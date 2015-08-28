# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('mp_id', models.IntegerField()),
                ('status', models.CharField(max_length=16)),
                ('status_detail', models.CharField(max_length=16)),
                ('created', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Preference',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('mp_id', models.CharField(max_length=46)),
                ('payment_url', models.URLField()),
                ('sandbox_url', models.URLField()),
                ('reference', models.TextField(unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='payment',
            name='preference',
            field=models.ForeignKey(to='mp.Preference', related_name='payments'),
        ),
    ]
