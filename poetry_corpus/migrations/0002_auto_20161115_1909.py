# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-15 16:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poetry_corpus', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='theme',
            options={'verbose_name': 'Тема', 'verbose_name_plural': 'Темы'},
        ),
        migrations.AddField(
            model_name='poem',
            name='accent_tagging',
            field=models.TextField(blank=True, default='', verbose_name='Разметка по ударениям'),
        ),
        migrations.AddField(
            model_name='poem',
            name='manually_tagged',
            field=models.BooleanField(default=False, verbose_name='Размечено руками'),
        ),
        migrations.AddField(
            model_name='poem',
            name='syllable_tagging',
            field=models.TextField(blank=True, default='', verbose_name='Слоговая разметка'),
        ),
    ]
