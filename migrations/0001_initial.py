# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('text', models.TextField()),
                ('score', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('group', models.CharField(max_length=2)),
                ('date', models.DateField()),
                ('status', models.CharField(max_length=64)),
                ('fullHTML', models.TextField()),
                ('problems', models.ManyToManyField(to='AIQGen.Problem')),
            ],
        ),
    ]
