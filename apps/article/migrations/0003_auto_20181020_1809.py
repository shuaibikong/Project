# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-10-20 18:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_article_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.TextField(default='', verbose_name='文章内容'),
        ),
    ]
