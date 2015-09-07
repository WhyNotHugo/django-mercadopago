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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(choices=[('o', 'Merchant Order'), ('p', 'Payment')], max_length=1)),
                ('resource_id', models.CharField(max_length=46)),
                ('processed', models.BooleanField(default=False)),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mp_id', models.CharField(max_length=46)),
                ('payment_url', models.URLField()),
                ('sandbox_url', models.URLField()),
                ('reference', models.CharField(max_length=128, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='payment',
            name='preference',
            field=models.ForeignKey(related_name='payments', to='mp.Preference'),
        ),
        migrations.AlterUniqueTogether(
            name='notification',
            unique_together=set([('topic', 'resource_id')]),
        ),
    ]
