# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-18 13:09
from __future__ import unicode_literals

from django.db import migrations
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_testimonialitem_fb'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testimonialitem',
            name='description',
            field=wagtail.wagtailcore.fields.RichTextField(),
        ),
    ]