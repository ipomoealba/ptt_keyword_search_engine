# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-09 04:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.IntegerField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('pid', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('content', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Content',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(blank=True, null=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.SmallIntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Gossiping',
            fields=[
                ('pid', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('ptime', models.DateTimeField()),
                ('arthor', models.CharField(max_length=30)),
                ('ip', models.CharField(blank=True, max_length=16, null=True)),
                ('content_keywords', models.TextField(blank=True, null=True)),
                ('comment_keywords', models.TextField(blank=True, null=True)),
                ('first_page', models.IntegerField()),
                ('relink', models.IntegerField()),
            ],
            options={
                'db_table': 'Gossiping',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='GossipingTest',
            fields=[
                ('pid', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('ptime', models.DateTimeField()),
                ('arthor', models.CharField(max_length=30)),
                ('ip', models.CharField(blank=True, max_length=16, null=True)),
                ('content_keywords', models.TextField(blank=True, null=True)),
                ('comment_keywords', models.TextField(blank=True, null=True)),
                ('first_page', models.IntegerField()),
                ('relink', models.IntegerField()),
            ],
            options={
                'db_table': 'Gossiping_test',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Keywords',
            fields=[
                ('pid', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('content_keywords', models.TextField(blank=True, null=True)),
                ('comment_keywords', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Keywords',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('pid', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('reply', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Reply',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tt',
            fields=[
                ('pid', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('ptime', models.DateTimeField()),
                ('arthor', models.CharField(max_length=30)),
                ('ip', models.CharField(blank=True, max_length=16, null=True)),
                ('content_keywords', models.TextField(blank=True, null=True)),
                ('comment_keywords', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'tt',
                'managed': False,
            },
        ),
    ]