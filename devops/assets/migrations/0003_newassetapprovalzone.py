# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-04-09 08:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0002_auto_20190402_1709'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewAssetApprovalZone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sn', models.CharField(max_length=128, unique=True, verbose_name='assetSNnum')),
                ('asset_type', models.CharField(blank=True, choices=[('server', 'SERVER'), ('networkdevice', 'NETWORKD'), ('storagedevice', 'STORAGED'), ('software', 'SOFT')], max_length=64, null=True)),
                ('model', models.CharField(blank=True, max_length=128, null=True)),
                ('ram_size', models.IntegerField(blank=True, null=True)),
                ('cpu_model', models.CharField(blank=True, max_length=128, null=True)),
                ('cpu_count', models.IntegerField(blank=True, null=True)),
                ('cpu_core_count', models.IntegerField(blank=True, null=True)),
                ('os_type', models.CharField(blank=True, max_length=64, null=True)),
                ('data', models.TextField(verbose_name='assetdata')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='reporttime')),
                ('approved', models.BooleanField(default=False, verbose_name='approved')),
                ('approved_date', models.DateTimeField(blank=True, null=True, verbose_name='approvetime')),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.UserProfile', verbose_name='approver')),
            ],
            options={
                'verbose_name': 'NewAssetApprovalasset',
                'verbose_name_plural': 'NewAssetApprovalasset',
            },
        ),
    ]
