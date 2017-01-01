# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-24 22:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('poetry_corpus', '0004_auto_20161116_1547'),
    ]

    operations = [
        migrations.CreateModel(
            name='Markup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, default='', verbose_name='Слоговая разметка по ударениям')),
                ('author', models.CharField(max_length=50, verbose_name='Автор разметки')),
            ],
            options={
                'verbose_name': 'Разметка',
                'verbose_name_plural': 'Разметки',
            },
        ),
        migrations.RemoveField(
            model_name='poem',
            name='accent_markup',
        ),
        migrations.RemoveField(
            model_name='poem',
            name='manually_tagged',
        ),
        migrations.AddField(
            model_name='markup',
            name='poem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='markups', to='poetry_corpus.Poem'),
        ),
    ]
