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

purCodeMain = "0005"


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

    loginInfo = request.session.get('loginInfo', "")
    adder = loginInfo["userId"]
    grade = loginInfo["grade"]
    sellerIdAll = loginInfo["sellerIdAll"]
    gradeForOther = grade
    if grade != 3:
        gradeForOther = 1

    return render(request, "system/role/index.html", locals())


# 保存数据（添加或修改）
@csrf_exempt
def ajaxSaveRole(request):
    data = request.POST
    try:
        with transaction.atomic():
            # print(data)
            if data != "":

                roleName = data["roleName"]
                memo = data["memo"]
                menuIdList = data["menuIdList"]
                loginInfo = request.session.get('loginInfo', "")
                adder = loginInfo["userId"]
                sellerId = loginInfo["sellerIdAll"]

                id = data["id"]

                if id == "" or id == "0":
                    # 判断是否有操作权限
                    purviewList = request.session.get('purviewList', [])  # 权限列表，list
                    purCode = "A" + purCodeMain
                    if purCode not in purviewList:
                        scription = "对不起！您<span style='color:red'>没有权限</span>添加此数据（" + purCode + "）"
                        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

                    # 判断唯一性（是否存在）

                    roles = models.Role.objects.filter(roleName=roleName,deletetime=None)
                    if sellerId>0:
                        roles.filter(sellerId=sellerId)
                    else:
                        roles.filter(sellerId=None)

                    if roles:
                        scription = "角色名称已经存在（" + roleName + "）"
                        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

                    sorts = 0
                    try:
                        model = models.Role.objects.filter(deletetime=None).latest("sorts")
                        if model:
                            sorts = model.sorts + 1
                        else:
                            sorts = 1
                    except models.Role.DoesNotExist:
                        sorts = 1

                    obj = models.Role.objects.create()
                    obj.roleName = roleName
                    obj.menuIdList =menuIdList
                    obj.memo = memo
                    if sellerId>0:
                        obj.sellerId=models.Seller.objects.filter(id=sellerId)[0]
                    obj.sorts = sorts
                    obj.adder = models.User.objects.filter(id=adder)[0]

                    count = obj.save()

                    #处理权限
                    models.RolePur.objects.filter(deletetime=None,roleId=None,adder=adder).update(roleId=obj)


                    #print(count)
                else:
                    # 判断是否有操作权限
                    purviewList = request.session.get('purviewList', [])  # 权限列表，list
                    purCode = "E" + purCodeMain
                    if purCode not in purviewList:
                        scription = "对不起！您<span style='color:red'>没有权限</span>修改此数据（" + purCode + "）"
                        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

                    # 判断唯一性（是否存在）

                    roles = models.Role.objects.exclude(id=id).filter(roleName=roleName, deletetime=None)
                    if sellerId>0:
                        roles.filter(sellerId=sellerId)
                    else:
                        roles.filter(sellerId=None)

                    if roles:
                        scription = "角色名称已经存在（" + roleName + "）"
                        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

                    count = models.Role.objects.filter(id=id).update(roleName=roleName, memo=memo, updatetime=datetime.now(),
                                                                     updater=models.User.objects.filter(id=adder)[0])

                scription = "操作成功，影响行数：" + str(count)
                return JsonResponse({"result": "T", "scription": scription, "extendInfo": "你的extendInfo"})
            else:
                scription = "提交参数错误！"
                return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})
    except Exception as e:
        #print(e)
        print(traceback.format_exc())
        scription = "执行时发生异常！（Exception）："+traceback.format_exc()
        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})


# 删除数据
@csrf_exempt
def ajaxDelRole(request):
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
                count = models.Role.objects.filter(id__in=idsList).update(deletetime=datetime.now(),
                                                                          deleter=models.User.objects.filter(id=deleter)[0])

            scription = "成功删除 " + str(count) + " 条数据！"
            return JsonResponse({"result": "T", "scription": scription, "extendInfo": "你的extendInfo"})
    except Exception as e:
        #print(e)
        scription = "执行时发生异常！（Exception）："+traceback.format_exc()
        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})


# gridData
@csrf_exempt
def gridDataRole(request):
    keywords = request.GET.get('keywords', '')
    userId = request.GET.get('userId', '')

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
    if loginInfo=="":
        returnData = {"total": -1,"errorInfo": "登录超时，请重新登录！！！", "rows": []}
        return HttpResponse(json.dumps(returnData))

    grade = loginInfo["grade"]
    sellerId = loginInfo["sellerIdAll"]

    if grade == 3:
        records = models.Role.objects.order_by(orderBy).filter(deletetime=None,sellerId=None)
    else:
        records = models.Role.objects.order_by(orderBy).filter(deletetime=None,sellerId=sellerId)

    if keywords != "":
        records = records.filter(
            Q(roleName__contains=keywords) | Q(memo__contains=keywords) | Q(menuIdList__contains=keywords))

    total = records.count()
    results = records[start:end]

    returnData = {"total": total, "rows": []}  #########非常重要############

    for result in results:

        defaultChecked = "F"
        #默认选中（用户设置角色时）
        if userId!="":
            if userId == "0":
                results = models.UserRole.objects.filter(deletetime=None, userId=None, roleId=result.id)
            else:
                results = models.UserRole.objects.filter(deletetime=None, userId=userId, roleId=result.id)
            if results.count()>0:
                defaultChecked = "T"

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
        returnData['rows'].append({
            "id": result.id,
            "roleName": str(result.roleName),
            "sellerId": str(result.sellerId),
            "memo": str(result.memo),
            "menuIdList": str(result.menuIdList),
            "sorts": str(result.sorts),
            "addtime": str(result.addtime),
            "updatetime": str(result.updatetime),
            "deletetime": str(result.deletetime),
            "adder": adder,
            "updater": updater,
            "deleter": deleter,
            "adderName": adderName,
            "updaterName": updaterName,
            "deleterName": deleterName,
            "defaultChecked": defaultChecked,
            # "addTime":  time.strftime("%Y-%m-%d %H:%M:%S %Z", time.gmtime(result.addTime)),
            # "PurchaseTime": time.strftime("%Y-%m-%d %H:%M:%S %Z", time.gmtime(results['purchasetime'])),
            # 将 时间戳 转换为 UTC时间
        })

    # 最后用dumps包装下，json.dumps({"rows": [{"gameorderid": 1}, {"gameorderid": 22}]})
    return HttpResponse(json.dumps(returnData))


# 排序
@csrf_exempt
def ajaxMoveSortsRole(request):
    id = request.POST.get("id", "")
    moveType = request.POST.get("moveType", "")

    try:
        with transaction.atomic():
            if id != "" and moveType != "":
                curRecord = models.Role.objects.get(id=id)
                if curRecord:
                    if moveType == "up":  # 上移
                        # 找到当前节点的上一个节点进行调换位置（排序位置）,如果找不到，说明当前已经是排在最上面的节点了，不做任何操作
                        preRecordQS = models.Role.objects.filter(sorts__lt=curRecord.sorts).order_by("-sorts")
                        if preRecordQS:  # 找到上一个
                            preRecord = preRecordQS[0]
                            models.Role.objects.filter(id=curRecord.id).update(sorts=preRecord.sorts)
                            models.Role.objects.filter(id=preRecord.id).update(sorts=curRecord.sorts)
                            scription = "上移成功！"
                            return JsonResponse({"result": "T", "scription": scription, "extendInfo": "你的extendInfo"})
                        else:
                            scription = "上移失败，已在顶部！"
                            return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})
                    else:  # 下移
                        nextRecordQS = models.Role.objects.filter(sorts__gt=curRecord.sorts).order_by("sorts")
                        if nextRecordQS:  # 找到下一个
                            nextRecord = nextRecordQS[0]
                            models.Role.objects.filter(id=curRecord.id).update(sorts=nextRecord.sorts)
                            models.Role.objects.filter(id=nextRecord.id).update(sorts=curRecord.sorts)
                            scription = "下移成功！"
                            return JsonResponse({"result": "T", "scription": scription, "extendInfo": "你的extendInfo"})
                        else:
                            scription = "下移失败，已在底部！"
                            return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})
    except Exception as e:
        #print(e)
        scription = "执行时发生异常！（Exception）："+traceback.format_exc()
        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})


#以下是额外的方法
#设置或取消角色可访问的菜单
@csrf_exempt
def setRoleMenu(request):
    roleId = request.POST.get("roleId", "")
    menuPur = request.POST.get("menuPur", "")

    try:
        with transaction.atomic():
            if roleId!="":
                count = models.Role.objects.filter(id=roleId).update(menuIdList=menuPur)
                scription = "设置成功！"
                return JsonResponse({"result": "T", "scription": scription, "extendInfo": "你的extendInfo"})
            else:
                scription = "设置失败！（参数错误:roleId）"
                return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

    except Exception as e:
        #print(e)
        scription = "执行时发生异常！（Exception）："+traceback.format_exc()
        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})


#设置（或取消）角色权限
@csrf_exempt
def setRolePur(request):
    roleId = request.POST.get("roleId", "")
    purcode = request.POST.get("purcode", "")
    purList = request.POST.get("purList", "")
    opType = request.POST.get("opType", "")
    # print(data)
    try:
        with transaction.atomic():
            if roleId != "":

                loginInfo = request.session.get('loginInfo', "")
                adder = loginInfo["userId"]
                sellerId = request.session.get('sellerId', "0")

                if purcode != "":
                    if opType == "set":#设置权限
                        if purList != "":
                            pList =  purList.split(",")
                            for pur in pList:
                                results = models.RolePur.objects.filter(deletetime=None,roleId=roleId,purcode=purcode,purview=pur)
                                if roleId == "0":
                                    results = results.filter(adder=models.User.objects.filter(id=adder)[0])
                                if (results.count()==0):
                                    obj = models.RolePur.objects.create()
                                    if roleId!="0":
                                        obj.roleId = models.Role.objects.filter(id=roleId)[0]
                                    obj.purcode = purcode
                                    obj.purview = pur
                                    obj.adder = models.User.objects.filter(id=adder)[0]
                                    count = obj.save()

                        scription = "设置成功！"
                        return JsonResponse({"result": "T", "scription": scription, "extendInfo": "你的extendInfo"})
                    else:#取消权限
                        if purList != "":
                            pList =  purList.split(",")
                            for pur in pList:
                                count = models.RolePur.objects.filter(roleId = roleId,purcode=purcode,purview=pur,deletetime=None).update(deletetime=datetime.now(),
                                                                                             deleter=models.User.objects.filter(id=adder)[0])
                        scription = "取消成功！"
                        return JsonResponse({"result": "T", "scription": scription, "extendInfo": "你的extendInfo"})

                else:
                    scription = "操作失败！（参数错误:purcode）"
                    return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

            else:
                scription = "操作失败！（参数错误:roleId）"
                return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})
    except Exception as e:
        # print(e)
        scription = "执行时发生异常！（Exception）：" + traceback.format_exc()
        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})


