# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-27 13:42
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField(verbose_name='Object ID')),
                ('comment', models.TextField(verbose_name='Comment')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
                ('is_removed', models.BooleanField(default=False, verbose_name='Is removed')),
                ('path', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(), editable=False, null=True, size=None)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType', verbose_name='Content type')),
                ('parent', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent_for_comment', to='comments.Comment', verbose_name='Parent')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name_plural': 'Comments',
                'ordering': ('path',),
                'permissions': (('remove_comment', 'Can remove comment'), ('remove_comment_tree', 'Can remove comment tree')),
                'verbose_name': 'Comment',
            },
        ),
    ]
