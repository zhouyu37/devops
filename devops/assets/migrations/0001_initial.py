# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-04-02 09:01
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset_type', models.CharField(choices=[('server', 'SERVER'), ('networkdevice', 'NETWORKD'), ('storagedevice', 'STORAGED'), ('software', 'SOFT')], default='server', max_length=64)),
                ('name', models.CharField(max_length=64, unique=True)),
                ('sn', models.CharField(max_length=128, unique=True, verbose_name='assetSNnum')),
                ('management_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='managerIP')),
                ('status', models.SmallIntegerField(choices=[(0, 'online'), (1, 'offline'), (2, 'unknown'), (3, 'fault'), (4, 'bak')], default=0)),
                ('remarks', models.TextField(blank=True, null=True, verbose_name='remarks')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'TotalAssets',
                'verbose_name_plural': 'TotalAssets',
            },
        ),
        migrations.CreateModel(
            name='BusinessUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='businessunit')),
                ('remarks', models.CharField(blank=True, max_length=64, verbose_name='remarks')),
                ('parent_unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent_level', to='assets.BusinessUnit')),
            ],
            options={
                'verbose_name': 'BusinessUnit',
                'verbose_name_plural': 'BusinessUnit',
            },
        ),
        migrations.CreateModel(
            name='CPU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpu_model', models.CharField(blank=True, max_length=128, verbose_name='CPUModel')),
                ('cpu_count', models.SmallIntegerField(verbose_name='CPUNum')),
                ('cpu_core_count', models.SmallIntegerField(verbose_name='CoreNum')),
                ('remarks', models.TextField(blank=True, null=True, verbose_name='remarks')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(blank=True, null=True)),
                ('asset', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='assets.Asset')),
            ],
            options={
                'verbose_name': 'CPU',
                'verbose_name_plural': 'CPU',
            },
        ),
        migrations.CreateModel(
            name='Disk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sn', models.CharField(blank=True, max_length=128, null=True, verbose_name='SNNum')),
                ('slot', models.CharField(max_length=64, verbose_name='DiskSlot')),
                ('model', models.CharField(blank=True, max_length=128, null=True, verbose_name='DiskType')),
                ('capacity', models.FloatField(verbose_name='DiskCapacityGB')),
                ('iface_type', models.CharField(choices=[('SATA', 'SATA'), ('SAS', 'SAS'), ('SCSI', 'SCSI'), ('SSD', 'SSD')], default='SAS', max_length=64, verbose_name='ifaceType')),
                ('remarks', models.TextField(blank=True, null=True, verbose_name='remarks')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(blank=True, null=True)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Asset')),
            ],
            options={
                'verbose_name': 'Disk',
                'verbose_name_plural': 'Disk',
            },
        ),
        migrations.CreateModel(
            name='EventLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='EventName')),
                ('event_type', models.SmallIntegerField(choices=[(1, 'devicechange'), (2, 'addplugins'), (3, 'deviceoffline'), (4, 'deviceonline'), (5, 'maintain'), (6, 'businessrelated'), (7, 'other')], verbose_name='EventType')),
                ('component', models.CharField(blank=True, max_length=255, null=True, verbose_name='EventChild')),
                ('detail', models.TextField(verbose_name='Detail')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='EventDate')),
                ('remarks', models.TextField(blank=True, null=True, verbose_name='remarks')),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Asset')),
            ],
            options={
                'verbose_name': 'EventLog',
                'verbose_name_plural': 'EventLog',
            },
        ),
        migrations.CreateModel(
            name='IDC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='IDCName')),
                ('remarks', models.CharField(blank=True, max_length=128, null=True, verbose_name='remarks')),
            ],
            options={
                'verbose_name': 'IDC',
                'verbose_name_plural': 'IDC',
            },
        ),
        migrations.CreateModel(
            name='NetworkDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_asset_type', models.SmallIntegerField(choices=[(0, 'switch'), (1, 'router'), (2, 'balancing'), (4, 'VPNdevice')], default=0, verbose_name='AssetType')),
                ('vlan_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='VlanIP')),
                ('intranet_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='InsideIP')),
                ('model', models.CharField(blank=True, max_length=128, null=True, verbose_name='Model')),
                ('port_num', models.SmallIntegerField(blank=True, null=True, verbose_name='PortNum')),
                ('asset', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='assets.Asset')),
            ],
            options={
                'verbose_name': 'NetworkDevice',
                'verbose_name_plural': 'NetworkDevice',
            },
        ),
        migrations.CreateModel(
            name='NIC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=64, null=True, verbose_name='NICName')),
                ('sn', models.CharField(blank=True, max_length=128, null=True, verbose_name='SNNum')),
                ('model', models.CharField(blank=True, max_length=128, null=True, verbose_name='NICType')),
                ('macaddress', models.CharField(max_length=64, unique=True, verbose_name='MAC')),
                ('ipaddress', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP')),
                ('netmask', models.CharField(blank=True, max_length=64, null=True)),
                ('bonding', models.CharField(blank=True, max_length=64, null=True)),
                ('remarks', models.CharField(blank=True, max_length=128, null=True, verbose_name='remarks')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(blank=True, null=True)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Asset')),
            ],
            options={
                'verbose_name': 'NIC',
                'verbose_name_plural': 'NIC',
            },
        ),
        migrations.CreateModel(
            name='RaidAdaptor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sn', models.CharField(blank=True, max_length=128, null=True, verbose_name='SN\u53f7')),
                ('slot', models.CharField(max_length=64, verbose_name='\u63d2\u53e3')),
                ('model', models.CharField(blank=True, max_length=64, null=True, verbose_name='\u578b\u53f7')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='\u5907\u6ce8')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(blank=True, null=True)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Asset')),
            ],
        ),
        migrations.CreateModel(
            name='RAM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sn', models.CharField(blank=True, max_length=128, null=True, verbose_name='SNNum')),
                ('model', models.CharField(max_length=128, verbose_name='RAMModel')),
                ('slot', models.CharField(max_length=64, verbose_name='RAMSlot')),
                ('capacity', models.IntegerField(verbose_name='RAMCapacity(MB)')),
                ('remarks', models.CharField(blank=True, max_length=128, null=True, verbose_name='remarks')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(blank=True, null=True)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Asset')),
            ],
            options={
                'verbose_name': 'RAM',
                'verbose_name_plural': 'RAM',
            },
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.CharField(choices=[('auto', 'Auto'), ('manual', 'Manual')], default='auto', max_length=32)),
                ('model', models.CharField(blank=True, max_length=128, null=True, verbose_name='Model')),
                ('raid_type', models.CharField(blank=True, max_length=512, null=True, verbose_name='RaidType')),
                ('os_type', models.CharField(blank=True, max_length=64, null=True, verbose_name='system')),
                ('asset', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='assets.Asset')),
            ],
            options={
                'verbose_name': 'Server',
                'verbose_name_plural': 'Server',
            },
        ),
        migrations.CreateModel(
            name='Software',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_asset_type', models.SmallIntegerField(choices=[(0, 'OS'), (1, 'destop\\develop software'), (2, 'business software')], default=0, verbose_name='sub_assset_type')),
                ('license_num', models.IntegerField(verbose_name='license_num')),
                ('version', models.CharField(help_text='eg. CentOS release 6.5 (Final)', max_length=64, unique=True, verbose_name='software/osVersion')),
            ],
            options={
                'verbose_name': 'software/os',
                'verbose_name_plural': 'software/os',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='Tag name')),
                ('create_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=32, verbose_name='name')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='tag',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.UserProfile'),
        ),
        migrations.AddField(
            model_name='networkdevice',
            name='firmware',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.Software'),
        ),
        migrations.AddField(
            model_name='eventlog',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.UserProfile', verbose_name='UserSource'),
        ),
        migrations.AddField(
            model_name='asset',
            name='admin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.UserProfile', verbose_name='manager'),
        ),
        migrations.AddField(
            model_name='asset',
            name='business_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.BusinessUnit', verbose_name='BusinessUnit'),
        ),
        migrations.AddField(
            model_name='asset',
            name='idc',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.IDC', verbose_name='IDC'),
        ),
        migrations.AlterUniqueTogether(
            name='ram',
            unique_together=set([('asset', 'slot')]),
        ),
        migrations.AlterUniqueTogether(
            name='raidadaptor',
            unique_together=set([('asset', 'slot')]),
        ),
        migrations.AlterUniqueTogether(
            name='nic',
            unique_together=set([('asset', 'macaddress')]),
        ),
        migrations.AlterUniqueTogether(
            name='disk',
            unique_together=set([('asset', 'slot')]),
        ),
    ]