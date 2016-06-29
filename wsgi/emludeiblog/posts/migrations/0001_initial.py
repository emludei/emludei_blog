# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=300, verbose_name='title')),
                ('body', models.TextField()),
                ('pub_date', models.DateTimeField(verbose_name='publication date', auto_now_add=True)),
            ],
            options={
                'ordering': ['-pub_date'],
                'verbose_name': 'post',
                'verbose_name_plural': 'posts',
            },
        ),
    ]
