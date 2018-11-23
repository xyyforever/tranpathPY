from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime
from django.db.models import Q
import json
from system import models
from system.helpClass import login_required
from django.db import transaction
import traceback

purCodeMain = "0002"


@login_required
def index(request):
    purviewList = request.session.get('purviewList', [])  # 权限列表，list
    purCode = "V" + purCodeMain
    if purCode in purviewList:
        allowV = "T"
    else:
        allowV = "F"

    purviewA = "F"
    purviewE = "F"
    purviewD = "F"
    if "A" + purCodeMain in purviewList:
        purviewA = "T"
    if "E" + purCodeMain in purviewList:
        purviewE = "T"
    if "D" + purCodeMain in purviewList:
        purviewD = "T"

    return render(request, "system/syspara/index.html", locals())


# 保存数据（添加或修改）
@csrf_exempt
def ajaxSaveSyspara(request):
    data = request.POST
    # print(data)
    try:
        with transaction.atomic():
            if data != "":
                paraType = data["paraType"]
                paraShow = data["paraShow"]
                paraTag = data["paraTag"]
                paraValue = data["paraValue"]
                memo = data["memo"]

                loginInfo = request.session.get('loginInfo', "")
                adder = loginInfo["userId"]

                id = data["id"]

                if id == "":
                    # 判断是否有操作权限
                    purviewList = request.session.get('purviewList', [])  # 权限列表，list
                    purCode = "A" + purCodeMain
                    if purCode not in purviewList:
                        scription = "对不起！您<span style='color:red'>没有权限</span>添加此数据（" + purCode + "）"
                        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

                    # 判断唯一性（是否存在）

                    model = models.Syspara.objects.filter(paraShow=paraShow, deletetime=None)
                    if model:
                        scription = "参数名称已经存在（" + paraShow + "）"
                        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})
                    model = models.Syspara.objects.filter(paraTag=paraTag, deletetime=None)
                    if model:
                        scription = "参数标志已经存在（" + paraTag + "）"
                        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

                    sorts = 0
                    try:
                        model = models.Syspara.objects.filter(deletetime=None).latest("sorts")
                        if model:
                            sorts = model.sorts + 1
                        else:
                            sorts = 1
                    except models.Syspara.DoesNotExist:
                        sorts = 1

                    obj = models.Syspara.objects.create()
                    obj.paraType = paraType
                    obj.paraShow = paraShow
                    obj.paraTag = paraTag
                    obj.paraValue = paraValue
                    obj.memo = memo
                    obj.sorts = sorts
                    obj.adder = models.User.objects.filter(id=adder)[0]

                    count = obj.save()
                else:
                    # 判断是否有操作权限
                    purviewList = request.session.get('purviewList', [])  # 权限列表，list
                    purCode = "E" + purCodeMain
                    if purCode not in purviewList:
                        scription = "对不起！您<span style='color:red'>没有权限</span>修改此数据（" + purCode + "）"
                        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

                    # 判断唯一性（是否存在）

                    model = models.Syspara.objects.exclude(id=id).filter(paraShow=paraShow, deletetime=None)
                    if model:
                        scription = "参数名称已经存在（" + paraShow + "）"
                        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})
                    model = models.Syspara.objects.exclude(id=id).filter(paraTag=paraTag, deletetime=None)
                    if model:
                        scription = "参数标志已经存在（" + paraTag + "）"
                        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

                    count = models.Syspara.objects.filter(id=id).update(paraType=paraType, paraShow=paraShow,paraTag=paraTag,paraValue=paraValue, memo=memo,updatetime=datetime.now(),updater=models.User.objects.filter(id=adder)[0])

                scription = "操作成功，影响行数：" + str(count)
                return JsonResponse({"result": "T", "scription": scription, "extendInfo": "你的extendInfo"})
            else:
                scription = "提交参数错误！"
                return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})
    except Exception as e:
        # print(e)
        scription = "执行时发生异常！（Exception）：" + traceback.format_exc()
        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})


# 删除数据
@csrf_exempt
def ajaxDelSyspara(request):
    try:
        with transaction.atomic():
            # 判断是否有操作权限
            purviewList = request.session.get('purviewList', [])  # 权限列表，list
            purCode = "D" + purCodeMain
            if purCode not in purviewList:
                scription = "对不起！您<span style='color:red'>没有权限</span>删除此数据（" + purCode + "）"
                return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

            idsForDelete = request.POST.get("idsForDelete", "")
            if idsForDelete != "":
                idsList = idsForDelete.strip(',').split(',')
                loginInfo = request.session.get('loginInfo', "")
                deleter = loginInfo["userId"]
                count = models.Syspara.objects.filter(id__in=idsList).update(deletetime=datetime.now(),deleter=models.User.objects.filter(id=deleter)[0])
            scription = "成功删除 " + str(count) + " 条数据！"
            return JsonResponse({"result": "T", "scription": scription, "extendInfo": "你的extendInfo"})
    except Exception as e:
        # print(e)
        scription = "执行时发生异常！（Exception）：" + traceback.format_exc()
        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})


# gridData
# @csrf_exempt
from basicInfo.helper import queryset_to_list
def gridDataSyspara(request):
    keywords = request.GET.get('keywords', '')
    sortName = request.GET.get('sortName', '')
    sortOrder = request.GET.get('sortOrder', '')
    orderBy = "-id"
    if sortName != "":
        if sortOrder == "" or sortOrder == "asc":
            orderBy = sortName
        else:
            orderBy = "-" + sortName

    '''服务端分页时，前端需要传回：limit（每页需要显示的数据量），offset（分页时 数据的偏移量，即第几页）'''
    '''mysql 利用 limit语法 进行分页查询'''
    '''服务端分页时，需要返回：total（数据总量），rows（每行数据）  如： {"total": total, "rows": []}'''

    pageIndex = request.GET.get('pageIndex', 1)
    pageSize = request.GET.get('pageSize', 20)
    start = (int(pageIndex) - 1) * int(pageSize)
    end = int(pageIndex) * int(pageSize)

    loginInfo = request.session.get('loginInfo', "")
    sellerId = loginInfo["sellerIdAll"]
    user_id = loginInfo['userId']
    user = models.User.objects.get(pk=user_id)
    print(user.id)
    records = user.paras.filter(deletetime=None)
    print(records)
    if keywords != "":
        records = records.filter(
            Q(paraType__contains=keywords) | Q(paraShow__contains=keywords) | Q(paraTag__contains=keywords) | Q(
                paraValue__contains=keywords) | Q(memo__contains=keywords))

    total = records.count()
    results = records[start:end]
    result_list = queryset_to_list(results)
    for result in result_list:
        if sellerId != 0:
            objs = models.SysparaForSeller.objects.filter(deletetime=None, sellerId=sellerId, sysparaId=result['id'])
            if objs.count() > 0:
                obj = objs[0]
                result['paraValue'] = str(obj.paraValue)
    returnData = {"total": total, "rows": result_list}  #########非常重要############
    # 最后用dumps包装下，json.dumps({"rows": [{"gameorderid": 1}, {"gameorderid": 22}]})
    return HttpResponse(json.dumps(returnData))

#弹出框获取
def grid_data_select(request):
    keywords = request.GET.get('keywords', '')
    sortName = request.GET.get('sortName', '')
    sortOrder = request.GET.get('sortOrder', '')
    orderBy = "-id"
    if sortName != "":
        if sortOrder == "" or sortOrder == "asc":
            orderBy = sortName
        else:
            orderBy = "-" + sortName

    '''服务端分页时，前端需要传回：limit（每页需要显示的数据量），offset（分页时 数据的偏移量，即第几页）'''
    '''mysql 利用 limit语法 进行分页查询'''
    '''服务端分页时，需要返回：total（数据总量），rows（每行数据）  如： {"total": total, "rows": []}'''

    pageIndex = request.GET.get('pageIndex', 1)
    pageSize = request.GET.get('pageSize', 20)
    start = (int(pageIndex) - 1) * int(pageSize)
    end = int(pageIndex) * int(pageSize)

    loginInfo = request.session.get('loginInfo', "")
    sellerId = loginInfo["sellerIdAll"]
    print(sellerId,type(sellerId))
    records = models.Syspara.objects.order_by(orderBy).filter(deletetime=None)
    if keywords != "":
        records = records.filter(
            Q(paraType__contains=keywords) | Q(paraShow__contains=keywords) | Q(paraTag__contains=keywords) | Q(
                paraValue__contains=keywords) | Q(memo__contains=keywords))

    total = records.count()
    results = records[start:end]
    result_list = queryset_to_list(results)
    for result in result_list:
        if sellerId != 0:
            objs = models.SysparaForSeller.objects.filter(deletetime=None, sellerId=sellerId, sysparaId=result['id'])
            if objs.count() > 0:
                obj = objs[0]
                result['paraValue'] = str(obj.paraValue)
    returnData = {"total": total, "rows": result_list}  #########非常重要############
    # 最后用dumps包装下，json.dumps({"rows": [{"gameorderid": 1}, {"gameorderid": 22}]})
    return HttpResponse(json.dumps(returnData))


# 排序
@csrf_exempt
def ajaxMoveSortsSyspara(request):
    id = request.POST.get("id", "")
    moveType = request.POST.get("moveType", "")

    try:
        with transaction.atomic():
            if id != "" and moveType != "":
                curRecord = models.Syspara.objects.get(id=id)
                if curRecord:
                    if moveType == "up":  # 上移
                        # 找到当前节点的上一个节点进行调换位置（排序位置）,如果找不到，说明当前已经是排在最上面的节点了，不做任何操作
                        preRecordQS = models.Syspara.objects.filter(sorts__lt=curRecord.sorts).order_by("-sorts")
                        if preRecordQS:  # 找到上一个
                            preRecord = preRecordQS[0]
                            models.Syspara.objects.filter(id=curRecord.id).update(sorts=preRecord.sorts)
                            models.Syspara.objects.filter(id=preRecord.id).update(sorts=curRecord.sorts)
                            scription = "上移成功！"
                            return JsonResponse({"result": "T", "scription": scription, "extendInfo": "你的extendInfo"})
                        else:
                            scription = "上移失败，已在顶部！"
                            return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})
                    else:  # 下移
                        nextRecordQS = models.Syspara.objects.filter(sorts__gt=curRecord.sorts).order_by("sorts")
                        if nextRecordQS:  # 找到下一个
                            nextRecord = nextRecordQS[0]
                            models.Syspara.objects.filter(id=curRecord.id).update(sorts=nextRecord.sorts)
                            models.Syspara.objects.filter(id=nextRecord.id).update(sorts=curRecord.sorts)
                            scription = "下移成功！"
                            return JsonResponse({"result": "T", "scription": scription, "extendInfo": "你的extendInfo"})
                        else:
                            scription = "下移失败，已在底部！"
                            return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

    except Exception as e:
        # print(e)
        scription = "执行时发生异常！（Exception）：" + traceback.format_exc()
        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})


# 以下是额外的方法
# 商家配置参数首页
@login_required
def indexForSeller(request):
    purCodeMain = "0009"

    purviewList = request.session.get('purviewList', [])  # 权限列表，list
    purCode = "V" + purCodeMain
    if purCode in purviewList:
        allowV = "T"
    else:
        allowV = "F"

    purviewA = "F"
    purviewE = "F"
    purviewD = "F"
    if "A" + purCodeMain in purviewList:
        purviewA = "T"
    if "E" + purCodeMain in purviewList:
        purviewE = "T"
    if "D" + purCodeMain in purviewList:
        purviewD = "T"

    return render(request, "system/syspara/indexForSeller.html", locals())


# 商家设置参数值提交
@csrf_exempt
def sellerSetValue(request):
    sysparaId = request.POST.get("sysparaId", "")
    paraValue = request.POST.get("paraValue", "")
    try:
        with transaction.atomic():
            loginInfo = request.session.get('loginInfo', "")
            adder = loginInfo["userId"]
            sellerId = loginInfo["sellerIdAll"]
            if sellerId != "" and sysparaId != "":
                objs = models.SysparaForSeller.objects.filter(deletetime=None, sellerId=sellerId, sysparaId=sysparaId)
                if objs.count() == 0:
                    obj = models.SysparaForSeller.objects.create()
                    obj.sysparaId = models.Syspara.objects.filter(id=sysparaId)[0]
                    obj.sellerId = models.Seller.objects.filter(id=sellerId)[0]
                    obj.paraValue = paraValue
                    obj.adder = models.User.objects.filter(id=adder)[0]
                    count = obj.save()
                else:
                    obj = objs[0]
                    count = models.SysparaForSeller.objects.filter(id=obj.id).\
                        update(paraValue=paraValue, updatetime=datetime.now(),
                               updater=models.User.objects.filter(id=adder)[0])
                scription = "操作成功！"
                return JsonResponse({"result": "T", "scription": scription, "extendInfo": "你的extendInfo"})
            else:
                scription = "参数错误！"
                return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

    except Exception as e:
        # print(e)
        scription = "执行时发生异常！（Exception）：" + traceback.format_exc()
        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})
