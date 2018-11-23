from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime
from django.db.models import Q
import json
from system import models
from system import helpClass
from system.helpClass import login_required
from django.db import transaction
import traceback


purCodeMain = "0008"

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

    return render(request, "system/informType/index.html", locals())


# 保存数据（添加或修改）
@csrf_exempt
def ajaxSaveInformType(request):
    data = request.POST
    # print(data)
    try:
        with transaction.atomic():
            if data != "":

                informName = data["informName"]
                informTag = data["informTag"]
                informInfo = data["informInfo"]
                condition = data["condition"]
                codePosition = data["codePosition"]
                paramMemo = data["paramMemo"]
                memo = data["memo"]

                loginInfo = request.session.get('loginInfo', "")
                adder = loginInfo["userId"]
                sellerId = loginInfo["sellerId"]

                id = data["id"]

                if id == "":
                    # 判断是否有操作权限
                    purviewList = request.session.get('purviewList', [])  # 权限列表，list
                    purCode = "A" + purCodeMain
                    if purCode not in purviewList:
                        scription = "对不起！您<span style='color:red'>没有权限</span>添加此数据（" + purCode + "）"
                        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

                    # 判断唯一性（是否存在）

                    model = models.InformType.objects.filter(informName=informName, deletetime=None)
                    if model:
                        scription = "消息名称已经存在（" + informName + "）"
                        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})
                    model = models.InformType.objects.filter(informTag=informTag, deletetime=None)
                    if model:
                        scription = "消息标志已经存在（" + informTag + "）"
                        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

                    obj = models.InformType.objects.create()
                    obj.informName = informName
                    obj.informTag = informTag
                    obj.informInfo = informInfo
                    obj.condition = condition
                    obj.codePosition = codePosition
                    obj.paramMemo = paramMemo
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

                    model = models.InformType.objects.exclude(id=id).filter(informName=informName, deletetime=None)
                    if model:
                        scription = "消息名称已经存在（" + informName + "）"
                        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})
                    model = models.InformType.objects.exclude(id=id).filter(informTag=informTag, deletetime=None)
                    if model:
                        scription = "消息标志已经存在（" + informTag + "）"
                        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

                    count = models.InformType.objects.filter(id=id).update(informName=informName, informTag=informTag,
                                                                           informInfo=informInfo, condition=condition,
                                                                           codePosition=codePosition,
                                                                           paramMemo=paramMemo, memo=memo,
                                                                           updatetime=datetime.now(),
                                                                           updater=models.User.objects.filter(id=adder)[
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
def ajaxDelInformType(request):
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
                count = models.InformType.objects.filter(id__in=idsList).update(deletetime=datetime.now(), deleter=
                models.User.objects.filter(id=deleter)[0])

            scription = "成功删除 " + str(count) + " 条数据！"
            return JsonResponse({"result": "T", "scription": scription, "extendInfo": "你的extendInfo"})
    except Exception as e:
        # print(e)
        traceback.print_exc()
        scription = "执行时发生异常！（Exception）：" + traceback.format_exc()
        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})


# gridData
@csrf_exempt
def gridDataInformType(request):
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

    records = models.InformType.objects.order_by(orderBy).filter(deletetime=None)
    if keywords != "":
        records = records.filter(
            Q(informName__contains=keywords) | Q(informTag__contains=keywords) | Q(informInfo__contains=keywords) | Q(
                condition__contains=keywords) | Q(codePosition__contains=keywords) | Q(
                paramMemo__contains=keywords) | Q(memo__contains=keywords))

    total = records.count()
    results = records[start:end]


    adder = loginInfo["userId"]
    sellerId = loginInfo["sellerIdAll"]

    returnData = {"total": total, "rows": []}  #########非常重要############

    for result in results:
        adder = 0
        updater = 0
        deleter = 0
        adderName = ""
        updaterName = ""
        deleterName = ""
        if result.adder != None:
            adder = result.adder.id
            adderName = result.adder.username
        if result.updater != None:
            updater = result.updater.id
            updaterName = result.updater.username
        if result.deleter != None:
            deleter = result.deleter.id
            deleterName = result.deleter.username

        targetUserList=""
        targetUserNameList = ""
        targetDeptList=""
        if sellerId>0:
            # 加载商家系统消息发送对象（用户）
            informTargetUsers = models.InformTargetUser.objects.filter(deletetime=None,sellerId=sellerId,informTypeId=result.id)
            if informTargetUsers.count()>0:
                for informTargetUser in informTargetUsers:
                    if targetUserList == "":
                        targetUserList = str(informTargetUser.userId.id)
                        targetUserNameList = informTargetUser.userId.username
                    else:
                        targetUserList = targetUserList + "," + str(informTargetUser.userId.id)
                        targetUserNameList = targetUserNameList + "," + informTargetUser.userId.username
            # 加载商家系统消息发送对象（部门）
            informTargetDepts = models.InformTargetDept.objects.filter(deletetime=None,sellerId=sellerId,informTypeId=result.id)
            if informTargetDepts.count()>0:
                for informTargetDept in informTargetDepts:
                    if targetDeptList == "":
                        targetDeptList = informTargetDept.deptName+":"+informTargetDept.positionList
                    else:
                        targetDeptList = targetDeptList + "|" + informTargetDept.deptName+":"+informTargetDept.positionList

        returnData['rows'].append({
            "id": result.id,
            "informName": str(result.informName),
            "informTag": str(result.informTag),
            "informInfo": str(result.informInfo),
            "condition": str(result.condition),
            "codePosition": str(result.codePosition),
            "paramMemo": str(result.paramMemo),
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
            "targetUserList":targetUserList,
            "targetUserNameList":targetUserNameList,
            "targetDeptList":targetDeptList,

            # "addTime":  time.strftime("%Y-%m-%d %H:%M:%S %Z", time.gmtime(result.addTime)),
            # "PurchaseTime": time.strftime("%Y-%m-%d %H:%M:%S %Z", time.gmtime(results['purchasetime'])),
            # 将 时间戳 转换为 UTC时间
        })

    # 最后用dumps包装下，json.dumps({"rows": [{"gameorderid": 1}, {"gameorderid": 22}]})
    return HttpResponse(json.dumps(returnData))


#以下为额外方法
#商家设置系统消息发送对象
def indexTarget(request):
    # request.POST
    # request.GET
    # return HttpResponse("Hello World!")
    # return render(request,"index.html")
    loginInfo = request.session.get('loginInfo', "")
    if loginInfo == "":
        return render(request, "system/login/login.html", locals())

    purCodeMain = "0011"

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

    loginInfo = request.session.get('loginInfo', "")
    adder = loginInfo["userId"]
    sellerId = loginInfo["sellerIdAll"]

    #获取用户
    condtion = {"parentSellerId":sellerId}
    userList = helpClass.getUserForSelect(**condtion)
    userJson = json.dumps(userList)

    #获取职位
    positionList = helpClass.getDicMainListForSelect(sellerId,"position")
    positionJson = json.dumps(positionList)

    #获取部门
    departmentList = helpClass.getDicMainListForSelect(sellerId, "department")

    return render(request, "system/informTarget/index.html", locals())


#提交设置系统消息发送对象
@csrf_exempt
def setInformTarget(request):
    data = request.POST
    # print(data)
    try:
        with transaction.atomic():
            if data != "":
                loginInfo = request.session.get('loginInfo', "")
                adder = loginInfo["userId"]
                sellerId = loginInfo["sellerIdAll"]

                informTypeId = data["informTypeId"]
                targetUserListStr = data["targetUserList"]
                departmentCount = data["departmentCount"]

                #设置接收系统消息部门开始
                deptNameList = []
                i = 0
                while(i < int(departmentCount)):
                    deptName = data["dept"+str(i)]
                    position = data["position"+str(i)]

                    #如果勾选了部门
                    if deptName!="":
                        #查找记录是否已在存在，如果不存在，则添加，反之则修改（更新）
                        records = models.InformTargetDept.objects.filter(deletetime=None,sellerId=sellerId,informTypeId=informTypeId,deptName=deptName)
                        if records.count()>0:
                            models.InformTargetDept.objects.filter(deletetime=None, sellerId=sellerId,
                                                                   informTypeId=informTypeId, deptName=deptName).update(positionList=position,
                                                                           updatetime=datetime.now(),
                                                                           updater=models.User.objects.filter(id=adder)[0])
                        else:
                            obj = models.InformTargetDept.objects.create()
                            obj.sellerId = models.Seller.objects.get(id=sellerId)
                            obj.informTypeId = models.InformType.objects.get(id=informTypeId)
                            obj.deptName = deptName
                            obj.positionList = position
                            obj.adder = models.User.objects.get(id=adder)
                            obj.save()
                        deptNameList.append(deptName)
                    i = i+1

                # 未勾选部门，删除记录
                models.InformTargetDept.objects.exclude(deptName__in=deptNameList).filter(deletetime=None,
                                                                                              sellerId=sellerId,
                                                                                              informTypeId=informTypeId).update(deletetime=datetime.now(), deleter=models.User.objects.filter(id=adder)[0])

                #设置接收系统消息部门结束

                #设置接收系统消息用户开始
                #1.删除现有记录
                models.InformTargetUser.objects.filter(deletetime=None,sellerId=sellerId,informTypeId=informTypeId).update(deletetime=datetime.now(), deleter=models.User.objects.filter(id=adder)[0])
                #2.添加新记录
                if targetUserListStr!="":
                    targetUserList = targetUserListStr.split(",")
                    for userId in targetUserList:
                        obj = models.InformTargetUser.objects.create()
                        obj.sellerId = models.Seller.objects.get(id=sellerId)
                        obj.informTypeId = models.InformType.objects.get(id=informTypeId)
                        obj.userId = models.User.objects.get(id=userId)
                        obj.adder = models.User.objects.get(id=adder)
                        obj.save()
                #设置接收系统消息用户结束

                scription = "操作成功！"
                return JsonResponse({"result": "T", "scription": scription, "extendInfo": "你的extendInfo"})
            else:
                scription = "提交参数错误！"
                return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})
    except Exception as e:
        # print(e)
        traceback.print_exc()
        scription = "执行时发生异常！（Exception）：" + traceback.format_exc()
        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})