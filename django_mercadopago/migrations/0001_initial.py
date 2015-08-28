# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('topic', models.CharField(max_length=1, choices=[('o', 'Merchant Order'), ('p', 'Payment')])),
                ('resource_id', models.CharField(max_length=46)),
                ('processed', models.BooleanField(default=False)),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('mp_id', models.IntegerField(unique=True)),
                ('status', models.CharField(max_length=16)),
                ('status_detail', models.CharField(max_length=16)),
                ('created', models.DateTimeField()),
                ('approved', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Preference',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
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
        migrations.AlterUniqueTogether(
            name='notification',
            unique_together=set([('topic', 'resource_id')]),
        ),
    ]
