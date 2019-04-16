# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from assets import models,admin,asset_handle
import json
import core
from assets import tables
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def asset_report(request):
    print(request.GET)
    if request.method == "POST":
        ass_handler=core.Asset(request)
        if ass_handler.data_is_valid():
            print(" asset data valid")
            ass_handler.data_inject()
        return HttpResponse(json.dumps(ass_handler.response))
    return HttpResponse("--test--")

@csrf_exempt
def asset_with_no_asset_id(request):
    if request.method == 'POST':
        ass_handler = core.Asset(request)
        res = ass_handler.get_asset_id_by_sn()
        # return render(request,'assets/acquire_asset_id_test.html',{'response':res})
        return HttpResponse(json.dumps(res))

@csrf_exempt
def new_assets_approval(request):
    if request.method == 'POST':
        print(request.POST)
        request.POST = request.POST.copy()
        approved_asset_list = request.POST.getlist('approved_asset_list')
        print("zhou",approved_asset_list)
        approved_asset_list = models.NewAssetApprovalZone.objects.filter(id__in=approved_asset_list)

        response_dic = {}
        for obj in approved_asset_list:
            request.POST['asset_data'] = obj.data
            ass_handler = core.Asset(request)
            if ass_handler.data_is_valid_without_id():
                ass_handler.data_inject()
                obj.approved = True
                obj.save()
            response_dic[obj.id] = ass_handler.response
        return render(request, 'assets/new_assets_approval.html',{'new_assets': approved_asset_list, 'response_dic': response_dic})
    else:
        ids = request.GET.get('ids')
        id_list = ids.split(',')
        new_assets = models.NewAssetApprovalZone.objects.filter(id__in=id_list)
        return render(request, 'assets/new_assets_approval.html', {'new_assets': new_assets})


def asset_list(request):
    print(request.GET)
    asset_obj_list = tables.table_filter(request, admin.AssetAdmin, models.Asset)
    # asset_obj_list = models.Asset.objects.all()
    print("asset_obj_list:", asset_obj_list)
    order_res = tables.get_orderby(request, asset_obj_list, admin.AssetAdmin)
    # print('----->',order_res)
    paginator = Paginator(order_res[0], admin.AssetAdmin.list_per_page)

    page = request.GET.get('page')
    try:
        asset_objs = paginator.page(page)
    except PageNotAnInteger:
        asset_objs = paginator.page(1)
    except EmptyPage:
        asset_objs = paginator.page(paginator.num_pages)

    table_obj = tables.TableHandler(request,
                                    models.Asset,
                                    admin.AssetAdmin,
                                    asset_objs,
                                    order_res
                                    )

    return render(request, 'assets/assets.html', {'table_obj': table_obj,'paginator': paginator})


def asset_detail(request, asset_id):
    if request.method == "GET":
        try:
            asset_obj = models.Asset.objects.get(id=asset_id)
        except ObjectDoesNotExist as e:
            return render(request, 'assets/asset_detail.html', {'error': e})
        return render(request, 'assets/asset_detail.html', {"asset_obj": asset_obj})

def get_asset_list(request):
    asset_dic = asset_handle.fetch_asset_list()
    print(asset_dic)

    return HttpResponse(json.dumps(asset_dic, default=utils.json_date_handler))

def asset_category(request):
    pass


from assets import rest_searializer
def api_test(request):
    if request.method == "GET":
        return render(request,"test_post.html")
    data=(request.POST.get("data"))
    print("test111",data)
    rest_obj = rest_searializer.AssetSerializer(data=data)
    # rest_obj = rest_searializer.AssetSerializer(data=data,many=True)
    print("lili",rest_obj.is_valid())
    ##the following  cannot  test successly
    if rest_obj.is_valid():
        rest_obj.save()
    return render(request,"test_post.html",{"data":rest_obj.data,"errors":rest_obj.errors})
