# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class UserProfile(User):
    name=models.CharField(u"name",max_length=32)
    def __str__(self):
        return self.name

class Asset(models.Model):
    asset_type_choices = (
        ('server', u'SERVER'),
        ('networkdevice', u'NETWORKD'),
        ('stormanagement_ipagedevice', u'STORAGED'),
        ('software', u'SOFT'),
    )
    asset_type = models.CharField(choices=asset_type_choices, max_length=64, default='server')
    name = models.CharField(max_length=64, unique=True)
    sn = models.CharField(u'assetSNnum', max_length=128, unique=True)
#   manufactory = models.ForeignKey('Manufactory', verbose_name=u'manufactory', null=True, blank=True)
    management_ip = models.GenericIPAddressField(u'managerIP', blank=True, null=True)
    business_unit = models.ForeignKey('BusinessUnit', verbose_name=u'BusinessUnit', null=True, blank=True)
#   tags = models.ManyToManyField('Tag', blank=True)
    admin = models.ForeignKey('UserProfile', verbose_name=u'manager', null=True, blank=True)
    idc = models.ForeignKey('IDC', verbose_name=u'IDC', null=True, blank=True)

    status_choices = ((0, 'online'),
                      (1, 'offline'),
                      (2, 'unknown'),
                      (3, 'fault'),
                      (4, 'bak'),
                      )
    status = models.SmallIntegerField(choices=status_choices, default=0)
    remarks = models.TextField(u'remarks', null=True, blank=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, auto_now=True)

    class Meta:
        verbose_name = 'TotalAssets'
        verbose_name_plural = "TotalAssets"

    def __str__(self):
        return 'id:%s-name:%s' % (self.id, self.name)

class Server(models.Model):
    asset = models.OneToOneField('Asset')
    # add server type
    created_by_choices = (
        ('auto', 'Auto'),
        ('manual', 'Manual'),
    )
    created_by = models.CharField(choices=created_by_choices, max_length=32,default='auto')
    # for vitural server
    #hosted_on = models.ForeignKey('self', related_name='hosted_on_server', blank=True, null=True)
    model = models.CharField(verbose_name=u'Model', max_length=128, null=True, blank=True)
    raid_type = models.CharField(u'RaidType', max_length=512, blank=True, null=True)
    os_type = models.CharField(u"system", max_length=64, blank=True, null=True)

    class Meta:
        verbose_name = 'Server'
        verbose_name_plural = "Server"

    def __str__(self):
        return '%s-sn:%s' % (self.asset.name, self.asset.sn)

class NetworkDevice(models.Model):
    asset = models.OneToOneField('Asset')
    sub_assset_type_choices = (
        (0, 'switch'),
        (1, 'router'),
        (2, 'balancing'),
        (4, 'VPNdevice'),
    )
    sub_asset_type = models.SmallIntegerField(choices=sub_assset_type_choices, verbose_name="AssetType", default=0)
    vlan_ip = models.GenericIPAddressField(u'VlanIP', blank=True, null=True)
    intranet_ip = models.GenericIPAddressField(u'InsideIP', blank=True, null=True)
    model = models.CharField(u'Model', max_length=128, null=True, blank=True)
    firmware = models.ForeignKey('Software', blank=True, null=True)
    port_num = models.SmallIntegerField(u'PortNum', null=True, blank=True)
#   device_detail = models.TextField(u'DeviceDetail', null=True, blank=True)

    class Meta:
        verbose_name = 'NetworkDevice'
        verbose_name_plural = "NetworkDevice"

class Software(models.Model):
    sub_assset_type_choices = (
        (0, 'OS'),
        (1, 'destop\develop software'),
        (2, 'business software'),
    )
    sub_asset_type = models.SmallIntegerField(choices=sub_assset_type_choices, verbose_name="sub_assset_type", default=0)
    license_num = models.IntegerField(verbose_name="license_num")
    version = models.CharField(u'software/osVersion', max_length=64, help_text=u'eg. CentOS release 6.5 (Final)', unique=True)

    class Meta:
        verbose_name = 'software/os'
        verbose_name_plural = "software/os"

    def __str__(self):
        return self.version

class CPU(models.Model):

    asset = models.OneToOneField('Asset')
    cpu_model = models.CharField(u'CPUModel', max_length=128, blank=True)
    cpu_count = models.SmallIntegerField(u'CPUNum')
    cpu_core_count = models.SmallIntegerField(u'CoreNum')
    remarks = models.TextField(u'remarks', null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'CPU'
        verbose_name_plural = "CPU"

    def __str__(self):
        return self.cpu_model

class RAM(models.Model):
    asset = models.ForeignKey('Asset')
    sn = models.CharField(u'SNNum', max_length=128, blank=True, null=True)
    model = models.CharField(u'RAMModel', max_length=128)
    slot = models.CharField(u'RAMSlot', max_length=64)
    capacity = models.IntegerField(u'RAMCapacity(MB)')
    remarks = models.CharField(u'remarks', max_length=128, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)
    class Meta:
        verbose_name = 'RAM'
        verbose_name_plural = "RAM"
        unique_together = ("asset", "slot")

    def __str__(self):
        return '%s:%s:%s' % (self.asset_id, self.slot, self.capacity)



    auto_create_fields = ['sn', 'slot', 'model', 'capacity']

class Disk(models.Model):
    asset = models.ForeignKey('Asset')
    sn = models.CharField(u'SNNum', max_length=128, blank=True, null=True)
    slot = models.CharField(u"DiskSlot", max_length=64)
    model = models.CharField(u'DiskType', max_length=128, blank=True, null=True)
    capacity = models.FloatField(u'DiskCapacityGB')
    disk_iface_choice = (
        ('SATA', 'SATA'),
        ('SAS', 'SAS'),
        ('SCSI', 'SCSI'),
        ('SSD', 'SSD'),
    )

    iface_type = models.CharField(u'ifaceType', max_length=64, choices=disk_iface_choice, default='SAS')
    remarks = models.TextField(u'remarks', blank=True, null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)

    auto_create_fields = ['sn', 'slot', 'model', 'capacity', 'iface_type']

    class Meta:
        unique_together = ("asset", "slot")
        verbose_name = 'Disk'
        verbose_name_plural = "Disk"

    def __str__(self):
        return '%s:slot:%s-capacity:%s' % (self.asset_id, self.slot, self.capacity)

class NIC(models.Model):
    asset = models.ForeignKey('Asset')
    name = models.CharField(u'NICName', max_length=64, blank=True, null=True)
    sn = models.CharField(u'SNNum', max_length=128, blank=True, null=True)
    model = models.CharField(u'NICType', max_length=128, blank=True, null=True)
    macaddress = models.CharField(u'MAC', max_length=64, unique=True)
    ipaddress = models.GenericIPAddressField(u'IP', blank=True, null=True)
    netmask = models.CharField(max_length=64, blank=True, null=True)
    bonding = models.CharField(max_length=64, blank=True, null=True)
    remarks = models.CharField(u'remarks', max_length=128, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = u'NIC'
        verbose_name_plural = u"NIC"
        unique_together = ("asset", "macaddress")
    def __str__(self):
        return '%s:%s' % (self.asset_id, self.macaddress)

    auto_create_fields = ['name', 'sn', 'model', 'macaddress', 'ipaddress', 'netmask', 'bonding']

class RaidAdaptor(models.Model):
    asset = models.ForeignKey('Asset')
    sn = models.CharField(u'SNNum', max_length=128, blank=True, null=True)
    slot = models.CharField(u'RaidSlot', max_length=64)
    model = models.CharField(u'RaidModel', max_length=64, blank=True, null=True)
    remarks = models.TextField(u'remarks', blank=True, null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("asset", "slot")

class BusinessUnit(models.Model):


    parent_unit = models.ForeignKey('self', related_name='parent_level', blank=True, null=True)
    name = models.CharField(u'businessunit', max_length=64, unique=True)

    # contact = models.ForeignKey('UserProfile',default=None)
    remarks = models.CharField(u'remarks', max_length=64, blank=True)

    class Meta:
        verbose_name = 'BusinessUnit'
        verbose_name_plural = "BusinessUnit"
    def __str__(self):
        return self.name

class IDC(models.Model):

    name = models.CharField(u'IDCName', max_length=64, unique=True)
    remarks = models.CharField(u'remarks', max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'IDC'
        verbose_name_plural = "IDC"

class Tag(models.Model):
    name = models.CharField('Tag name', max_length=32, unique=True)
    creator = models.ForeignKey('UserProfile')
    create_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class EventLog(models.Model):

    name = models.CharField(u'EventName', max_length=100)
    event_type_choices = (
        (1, u'devicechange'),
        (2, u'addplugins'),
        (3, u'deviceoffline'),
        (4, u'deviceonline'),
        (5, u'maintain'),
        (6, u'businessrelated'),
        (7, u'other'),
    )
    event_type = models.SmallIntegerField(u'EventType', choices=event_type_choices)
    asset = models.ForeignKey('Asset')
    component = models.CharField('EventChild', max_length=255, blank=True, null=True)
    detail = models.TextField(u'Detail')
    date = models.DateTimeField(u'EventDate', auto_now_add=True)
    user = models.ForeignKey('UserProfile', verbose_name=u'UserSource')
    remarks = models.TextField(u'remarks', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'EventLog'
        verbose_name_plural = "EventLog"

    # def colored_event_type(self):
    #     if self.event_type == 1:
    #         cell_html = '<span style="background: orange;">%s</span>'
    #     elif self.event_type == 2:
    #         cell_html = '<span style="background: yellowgreen;">%s</span>'
    #     else:
    #         cell_html = '<span >%s</span>'
    #     return cell_html % self.get_event_type_display()
    #
    # colored_event_type.allow_tags = True
    # colored_event_type.short_description = u'EventType'

class NewAssetApprovalZone(models.Model):

    sn = models.CharField(u'assetSNnum', max_length=128, unique=True)
    asset_type_choices = (
        ('server', u'SERVER'),
        ('networkdevice', u'NETWORKD'),
        ('storagedevice', u'STORAGED'),
        ('software', u'SOFT'),
    )
    asset_type = models.CharField(choices=asset_type_choices, max_length=64, blank=True, null=True)
    model = models.CharField(max_length=128, blank=True, null=True)
    ram_size = models.IntegerField(blank=True, null=True)
    cpu_model = models.CharField(max_length=128, blank=True, null=True)
    cpu_count = models.IntegerField(blank=True, null=True)
    cpu_core_count = models.IntegerField(blank=True, null=True)
    os_type = models.CharField(max_length=64, blank=True, null=True)
    data = models.TextField(u'assetdata')
    date = models.DateTimeField(u'reporttime', auto_now_add=True)
    approved = models.BooleanField(u'approved', default=False)
    approved_by = models.ForeignKey('UserProfile', verbose_name=u'approver', blank=True, null=True)
    approved_date = models.DateTimeField(u'approvetime', blank=True, null=True)
    def __str__(self):
        return self.sn

    class Meta:
        verbose_name = 'NewAssetApprovalasset'
        verbose_name_plural = "NewAssetApprovalasset"