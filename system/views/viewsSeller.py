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

purCodeMain = "0007"

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

    return render(request, "system/seller/index.html", locals())


# 保存数据（添加或修改）
@csrf_exempt
def ajaxSaveSeller(request):
    data = request.POST
    # print(data)
    try:
        with transaction.atomic():
            if data != "":
                sellerName = data["sellerName"]
                sellerAddress = data["sellerAddress"]
                sellerLinkman = data["sellerLinkman"]
                sellerTel = data["sellerTel"]
                employeeSnGType = data["employeeSnGType"]
                sellerType = data["sellerType"]
                status = data["status"]
                memo = data["memo"]

                loginInfo = request.session.get('loginInfo', "")
                adder = loginInfo["userId"]
                sellerId = request.session.get('sellerId', "")

                id = data["id"]

                if id == "":
                    # 判断是否有操作权限
                    purviewList = request.session.get('purviewList', [])  # 权限列表，list
                    purCode = "A" + purCodeMain
                    if purCode not in purviewList:
                        scription = "对不起！您<span style='color:red'>没有权限</span>添加此数据（" + purCode + "）"
                        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

                    # 判断唯一性（是否存在）

                    model = models.Seller.objects.filter(sellerName=sellerName, deletetime=None)
                    if model:
                        scription = "商家（供应商）名称已经存在（" + sellerName + "）"
                        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

                    obj = models.Seller.objects.create()
                    obj.sellerName = sellerName
                    obj.sellerAddress = sellerAddress
                    obj.sellerLinkman = sellerLinkman
                    obj.sellerTel = sellerTel
                    obj.employeeSnGType = employeeSnGType
                    obj.sellerType = sellerType
                    obj.status = status
                    obj.memo = memo
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

                    model = models.Seller.objects.exclude(id=id).filter(sellerName=sellerName, deletetime=None)
                    if model:
                        scription = "商家（供应商）名称已经存在（" + sellerName + "）"
                        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

                    count = models.Seller.objects.filter(id=id).update(sellerName=sellerName, sellerAddress=sellerAddress,
                                                                       sellerLinkman=sellerLinkman, sellerTel=sellerTel,
                                                                       employeeSnGType=employeeSnGType, sellerType=sellerType,
                                                                       status=status, memo=memo, updatetime=datetime.now(),
                                                                       updater=models.User.objects.filter(id=adder)[0])

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
def ajaxDelSeller(request):
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
                count = models.Seller.objects.filter(id__in=idsList).update(deletetime=datetime.now(),
                                                                            deleter=models.User.objects.filter(id=deleter)[0])

            scription = "成功删除 " + str(count) + " 条数据！"
            return JsonResponse({"result": "T", "scription": scription, "extendInfo": "你的extendInfo"})
    except Exception as e:
        #print(e)
        scription = "执行时发生异常！（Exception）："+traceback.format_exc()
        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

# gridData
@csrf_exempt
def gridDataSeller(request):
    keywords = request.GET.get('keywords', '')
    parentSellerId = request.GET.get('keywords', '')
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
        returnData = {"total": -1,"errorInfo": "登录超时，请重新登录！！！", "rows": []}
        return HttpResponse(json.dumps(returnData))

    if parentSellerId=="":
        records = models.Seller.objects.order_by(orderBy).filter(deletetime=None,parentSellerId=None)
    else:
        records = models.Seller.objects.order_by(orderBy).filter(deletetime=None, parentSellerId=parentSellerId)
    if keywords != "":
        records = records.filter(Q(sellerName__contains=keywords) | Q(uniqueCode__contains=keywords) | Q(
            sellerAddress__contains=keywords) | Q(sellerLinkman__contains=keywords) | Q(
            sellerTel__contains=keywords) | Q(employeeSnGType__contains=keywords) | Q(
            sellerType__contains=keywords) | Q(status__contains=keywords) | Q(memo__contains=keywords))

    total = records.count()


    returnData = {"total": total, "rows": []}  #########非常重要############

    if total>0:
        results = records[start:end]
        for result in results:
            userId = 0
            adder = 0
            updater = 0
            deleter = 0
            userIdName = ""
            adderName = ""
            updaterName = ""
            deleterName = ""
            if result.userId!=None:
                userId = result.userId.id
                userIdName=result.userId.username
            if result.adder != None:
                adder = result.adder.id
                adderName = result.adder.username
            if result.updater != None:
                updater = result.updater.id
                updaterName = result.updater.username
            if result.deleter != None:
                deleter = result.deleter.id
                deleterName = result.deleter.username
            returnData['rows'].append({
                "id": result.id,
                "sellerName": str(result.sellerName),
                "userId": str(userId),
                "userIdName": userIdName,
                "uniqueCode": str(result.uniqueCode),
                "sellerAddress": str(result.sellerAddress),
                "sellerLinkman": str(result.sellerLinkman),
                "sellerTel": str(result.sellerTel),
                "employeeSnGType": str(result.employeeSnGType),
                "sellerType": str(result.sellerType),
                "status": str(result.status),
                "memo": str(result.memo),
                "addtime": str(result.addtime),
                "updatetime": str(result.updatetime),
                "deletetime": str(result.deletetime),
                "adder": adder,
                "updater": updater,
                "deleter": deleter,
                "adderName": adderName,
                "updaterName": updaterName,
                "deleterName": deleterName,
                # "addTime":  time.strftime("%Y-%m-%d %H:%M:%S %Z", time.gmtime(result.addTime)),
                # "PurchaseTime": time.strftime("%Y-%m-%d %H:%M:%S %Z", time.gmtime(results['purchasetime'])),
                # 将 时间戳 转换为 UTC时间
            })

    # 最后用dumps包装下，json.dumps({"rows": [{"gameorderid": 1}, {"gameorderid": 22}]})
    return HttpResponse(json.dumps(returnData))




