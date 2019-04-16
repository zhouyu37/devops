# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from assets import models

class ServerInline(admin.TabularInline):
    model = models.Server

class CPUInline(admin.TabularInline):
    model = models.CPU
    exclude = ('remarks',)
    readonly_fields = ['create_date']


class AssetAdmin(admin.ModelAdmin):
    list_display = ('id','asset_type','sn','name','management_ip','idc','business_unit','admin','status')
    inlines = [ServerInline,CPUInline]
    search_fields = ['sn',]
    choice_fields = ('asset_type', 'status')
    fk_fields = ( 'idc', 'business_unit', 'admin')
    list_per_page = 10
    list_filter = ('asset_type','status','idc','business_unit','admin')
    dynamic_fk = 'asset_type'
    dynamic_list_display = ('model','sub_asset_type','os_type')
    dynamic_choice_fields = ('sub_asset_type',)
    m2m_fields = ('tags',)

from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
class NewAssetApprovalZoneAdmin(admin.ModelAdmin):
    list_display = ('sn','asset_type','model','cpu_model','cpu_count','cpu_core_count','ram_size','os_type','date','approved','approved_by','approved_date')
    actions = ['approve_selected_objects']
    def approve_selected_objects(modeladmin, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        ct = ContentType.objects.get_for_model(queryset.model)
        return HttpResponseRedirect("/asset/new_assets/approval/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))
    approve_selected_objects.short_description = "approvetoDB"



admin.site.register(models.UserProfile)
admin.site.register(models.Asset,AssetAdmin)
admin.site.register(models.Server)
admin.site.register(models.NetworkDevice)
admin.site.register(models.Software)
admin.site.register(models.CPU)
admin.site.register(models.RAM)
admin.site.register(models.Disk)
admin.site.register(models.NIC)
admin.site.register(models.RaidAdaptor)
admin.site.register(models.BusinessUnit)
admin.site.register(models.IDC)
admin.site.register(models.Tag)
admin.site.register(models.EventLog)
admin.site.register(models.NewAssetApprovalZone,NewAssetApprovalZoneAdmin)
