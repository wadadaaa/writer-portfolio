# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-01 07:51
from __future__ import unicode_literals

from django.db import migrations
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20160130_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productitem',
            name='description',
            field=wagtail.wagtailcore.fields.RichTextField(),
        ),
    ]