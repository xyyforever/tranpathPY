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
from django.db import transaction
import traceback


# purCodeMain = "-1"

def index(request):
    # request.POST
    # request.GET
    # return HttpResponse("Hello World!")
    # return render(request,"index.html")
    loginInfo = request.session.get('loginInfo', "")
    sellerId = loginInfo["sellerIdAll"]
    #已绑定
    bindSellerList = modelsbasicInfo.BindSeller.objects.filter(deletetime=None,sellerId=sellerId)
    #被绑定
    bundSellerList = modelsbasicInfo.BindSeller.objects.filter(deletetime=None, bindSellerId=sellerId)

    if loginInfo == "":
        return render(request, "system/login/login.html", locals())

    # purviewList = request.session.get('purviewList', [])  # 权限列表，list
    # purCode = "V"+purCodeMain
    # if purCode in purviewList:
    #    allowV = "T"
    # else:
    #    allowV = "F"

    # purviewA = "F"
    # purviewE = "F"
    # purviewD = "F"
    # if "A" + purCodeMain in purviewList:
    #    purviewA = "T"
    # if "E" + purCodeMain in purviewList:
    #    purviewE = "T"
    # if "D" + purCodeMain in purviewList:
    #    purviewD = "T"

    allowV = "T"
    purviewA = "T"
    purviewE = "T"
    purviewD = "T"

    return render(request, "basicInfo/bindSeller/index.html", locals())


# 保存数据（添加或修改）
@csrf_exempt
def ajaxSaveBindSeller(request):
    data = request.POST
    # print(data)
    try:
        with transaction.atomic():
            if data != "":

                sellerName = data["sellerName"]
                memo = data["memo"]

                loginInfo = request.session.get('loginInfo', "")
                adder = loginInfo["userId"]
                sellerId = loginInfo["sellerIdAll"]

                objs = models.Seller.objects.filter(deletetime=None,sellerName=sellerName)
                if objs.count()>0:
                    sellerForBind = objs[0]
                    if sellerId == sellerForBind.id:
                        scription = "不允许绑定当前登录商家（自身）！（商家全称：" + sellerName + "）"
                        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})
                    else:
                        #判断是否已绑定过
                        records = modelsbasicInfo.BindSeller.objects.filter(deletetime=None,sellerId=sellerId,bindSellerId=sellerForBind.id);
                        if records.count()>0:
                            scription = "该商家已绑定！（商家全称：" + sellerName + "）"
                            return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})
                        else:
                            obj = modelsbasicInfo.BindSeller.objects.create()
                            obj.bindSellerId = sellerForBind
                            obj.memo = memo
                            if sellerId > 0:
                                obj.sellerId = models.Seller.objects.filter(id=sellerId)[0]
                            obj.adder = models.User.objects.filter(id=adder)[0]

                            count = obj.save()
                else:
                    scription = "未找到商家！（商家全称："+sellerName+"）"
                    return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})


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
def ajaxDelBindSeller(request):
    data = request.POST
    idsForDelete = data["bindSellerId"]
    try:
        with transaction.atomic():
            # 判断是否有操作权限
            # purviewList = request.session.get('purviewList', [])  # 权限列表，list
            # purCode = "D" + purCodeMain
            # if purCode not in purviewList:
            #    scription = "对不起！您<span style='color:red'>没有权限</span>删除此数据（" + purCode + "）"
            #    return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

            count = 0
            if idsForDelete != "":
                idsList = idsForDelete.strip(',').split(',')
                loginInfo = request.session.get('loginInfo', "")
                deleter = loginInfo["userId"]
                count = modelsbasicInfo.BindSeller.objects.filter(id__in=idsList).update(deletetime=datetime.now(),
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
def gridDataBindSeller(request):
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

    records = modelsbasicInfo.BindSeller.objects.order_by(orderBy).filter(deletetime=None)
    if keywords != "":
        records = records.filter(Q(memo__contains=keywords))

    total = records.count()
    results = records[start:end]
    list_results = queryset_to_list(results)
    returnData = {"total": total, "rows": list_results}  #########非常重要############

    # 最后用dumps包装下，json.dumps({"rows": [{"gameorderid": 1}, {"gameorderid": 22}]})
    return HttpResponse(json.dumps(returnData))




