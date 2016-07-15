# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-18 12:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_testimonialitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePageTestimonialItem',
            fields=[
                ('testimonialitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.TestimonialItem')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='testimonial_items', to='home.HomePage')),
            ],
            options={
                'abstract': False,
                'ordering': ['sort_order'],
            },
            bases=('home.testimonialitem', models.Model),
        ),
    ]
