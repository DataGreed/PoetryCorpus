# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-26 14:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corpus', '0013_markupversion_is_manual'),
    ]

    operations = [
        migrations.AddField(
            model_name='poem',
            name='is_standard',
            field=models.BooleanField(default=False, verbose_name='Эталонные (проверенные) стихи'),
        ),
    ]
