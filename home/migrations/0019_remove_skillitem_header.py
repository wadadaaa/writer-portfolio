# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-16 16:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_remove_homepageintroitem_embed_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skillitem',
            name='header',
        ),
    ]