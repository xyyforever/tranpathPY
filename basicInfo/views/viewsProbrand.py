from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime
from django.db.models import Q
import json
from system import models
from basicInfo import models as modelsbasicInfo
from system import helpClass
from system.helpClass import login_required
from django.db import transaction
import traceback
from django.core import serializers
purCodeMain = "0013"

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

    return render(request, "basicInfo/probrand/index.html", locals())


# 保存数据（添加或修改）
@csrf_exempt
def ajaxSaveProbrand(request):
    data = request.POST
    # print(data)
    try:
        with transaction.atomic():
            if data != "":

                c_name = data["c_name"]
                e_name = data["e_name"]
                name_head = data["name_head"]
                from_country = data["from_country"]
                info = data["info"]

                loginInfo = request.session.get('loginInfo', "")
                adder = loginInfo["userId"]
                sellerId = loginInfo["sellerIdAll"]

                id = data["id"]

                if id == "":
                    # 判断是否有操作权限
                    purviewList = request.session.get('purviewList', [])  # 权限列表，list
                    purCode = "A" + purCodeMain
                    if purCode not in purviewList:
                        scription = "对不起！您<span style='color:red'>没有权限</span>添加此数据（" + purCode + "）"
                        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

                    # 判断唯一性（是否存在）

                    probrands = modelsbasicInfo.Probrand.objects.filter(c_name=c_name, deletetime=None)

                    if probrands:
                        scription = "中文名%s已经存在" %c_name
                        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})
                    probrands = modelsbasicInfo.Probrand.objects.filter(e_name=e_name, deletetime=None)

                    if probrands:
                        scription = "音文名%s已经存在" %e_name
                        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

                    obj = modelsbasicInfo.Probrand.objects.create()
                    obj.c_name = c_name
                    obj.e_name = e_name
                    obj.name_head = name_head
                    obj.from_country = from_country
                    obj.info = info

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

                    probrands = modelsbasicInfo.Probrand.objects.exclude(id=id).filter(c_name=c_name, deletetime=None)

                    if probrands:
                        scription = "中文名已经存在（" + c_name + "）"
                        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})
                    probrands = modelsbasicInfo.Probrand.objects.exclude(id=id).filter(e_name=e_name, deletetime=None)

                    if probrands:
                        scription = "音文名已经存在（" + e_name + "）"
                        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

                    count = modelsbasicInfo.Probrand.objects.filter(id=id).update(c_name=c_name, e_name=e_name,
                                                                                  name_head=name_head,
                                                                                  from_country=from_country, info=info,
                                                                                  updatetime=datetime.now(), updater=
                                                                                  models.User.objects.filter(id=adder)[
                                                                                      0])

                scription = "操作成功，影响行数：" + str(count)
                return JsonResponse({"result": "T", "scription": scription, "extendInfo": "你的extendInfo"})
            else:
                scription = "提交参数错误！"
                return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})
    except Exception as e:
        # print(e)
        traceback.print_exc()
        scription = "执行时发生异常！（Exception）：" + traceback.format_exc()
        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})


# 删除数据
@csrf_exempt
def ajaxDelProbrand(request):
    try:
        with transaction.atomic():
            # 判断是否有操作权限
            purviewList = request.session.get('purviewList', [])  # 权限列表，list
            purCode = "D" + purCodeMain
            if purCode not in purviewList:
                scription = "对不起！您<span style='color:red'>没有权限</span>删除此数据（" + purCode + "）"
                return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

            count = 0
            idsForDelete = request.POST.get("idsForDelete", "")
            if idsForDelete != "":
                idsList = idsForDelete.strip(',').split(',')
                loginInfo = request.session.get('loginInfo', "")
                deleter = loginInfo["userId"]
                count = modelsbasicInfo.Probrand.objects.filter(id__in=idsList).update(deletetime=datetime.now(),
                                                                                       deleter=
                                                                                       models.User.objects.filter(
                                                                                           id=deleter)[0])

            scription = "成功删除 " + str(count) + " 条数据！"
            return JsonResponse({"result": "T", "scription": scription, "extendInfo": "你的extendInfo"})
    except Exception as e:
        # print(e)
        traceback.print_exc()
        scription = "执行时发生异常！（Exception）：" + traceback.format_exc()
        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})


# gridData
from basicInfo.helper import queryset_to_list
@csrf_exempt
def gridDataProbrand(request):
    keywords = request.GET.get('keywords', '')
    # sortName = tableName & sortOrder = desc

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
    # print(pageIndex)
    start = (int(pageIndex) - 1) * int(pageSize)
    end = int(pageIndex) * int(pageSize)

    loginInfo = request.session.get('loginInfo', "")
    if loginInfo == "":
        returnData = {"total": -1, "errorInfo": "登录超时，请重新登录！！！", "rows": []}
        return HttpResponse(json.dumps(returnData))

    grade = loginInfo["grade"]
    sellerId = loginInfo["sellerIdAll"]

    records = modelsbasicInfo.Probrand.objects.order_by(orderBy).filter(deletetime=None)
    if keywords != "":
        records = records.filter(
            Q(c_name__contains=keywords) | Q(e_name__contains=keywords) | Q(name_head__contains=keywords) | Q(
                from_country__contains=keywords) | Q(info__contains=keywords))

    total = records.count()
    results = records[start:end]
    list_results = queryset_to_list(results)
    returnData = {"total": total, "rows": list_results}  #########非常重要############

    # 最后用dumps包装下，json.dumps({"rows": [{"gameorderid": 1}, {"gameorderid": 22}]})
    return JsonResponse(returnData)




