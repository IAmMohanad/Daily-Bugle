# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-16 18:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('text', models.TextField()),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('article_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.Article')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isLike', models.NullBooleanField()),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('article_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.Article')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='like',
            name='author_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.User'),
        ),
        migrations.AddField(
            model_name='comment',
            name='author_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.User'),
        ),
        migrations.AddField(
            model_name='article',
            name='author_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.User'),
        ),
        migrations.AddField(
            model_name='article',
            name='category_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.Category'),
        ),
    ]
