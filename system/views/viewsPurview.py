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

purCodeMain = "0004"


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

    return render(request, "system/purview/index.html", locals())


# 保存数据（添加或修改）
@csrf_exempt
def ajaxSavePurview(request):
    data = request.POST
    # print(data)
    try:
        with transaction.atomic():
            if data != "":
                purname = data["purname"]
                grade = data["grade"]
                purcode = data["purcode"]
                memo = data["memo"]

                loginInfo = request.session.get('loginInfo', "")
                adder = loginInfo["userId"]
                sellerId = request.session.get('sellerId', "")

                id = data["id"]

                if id == "":
                    # 判断是否有操作权限
                    purviewList = request.session.get("purviewList", [])  # 权限列表，list

                    purCode = "A" + purCodeMain
                    if purCode not in purviewList:
                        scription = "对不起！您<span style='color:red'>没有权限</span>添加此数据（" + purCode + "）"
                        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

                    # 判断唯一性（是否存在）

                    model = models.Purview.objects.filter(purname=purname, deletetime=None)
                    if model:
                        scription = "权限名称已经存在（" + purname + "）"
                        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})
                    model = models.Purview.objects.filter(purcode=purcode, deletetime=None)
                    if model:
                        scription = "权限代码已经存在（" + purcode + "）"
                        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

                    sorts = 0
                    try:
                        model = models.Purview.objects.filter(deletetime=None).latest("sorts")
                        if model:
                            sorts = model.sorts + 1
                        else:
                            sorts = 1
                    except models.Purview.DoesNotExist:
                        sorts = 1

                    obj = models.Purview.objects.create()
                    obj.purname = purname
                    obj.grade = grade
                    obj.purcode = purcode
                    obj.memo = memo
                    obj.sorts = sorts
                    obj.adder = models.User.objects.filter(id=adder)[0]

                    count = obj.save()
                else:
                    # 判断是否有操作权限
                    purviewList = request.session.get('purviewList', [])  # 权限列表，list
                    #print("AAAAAAAAAAAAAA")
                    #print(purviewList)
                    #print("AAAAAAAAAAAAAA")
                    purCode = "E" + purCodeMain
                    if purCode not in purviewList:
                        scription = "对不起！您<span style='color:red'>没有权限</span>修改此数据（" + purCode + "）"
                        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

                    # 判断唯一性（是否存在）

                    model = models.Purview.objects.exclude(id=id).filter(purname=purname, deletetime=None)
                    if model:
                        scription = "权限名称已经存在（" + purname + "）"
                        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})
                    model = models.Purview.objects.exclude(id=id).filter(purcode=purcode, deletetime=None)
                    if model:
                        scription = "权限代码已经存在（" + purcode + "）"
                        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

                    count = models.Purview.objects.filter(id=id).update(purname=purname, grade=grade, purcode=purcode,
                                                                        memo=memo, updatetime=datetime.now(),
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
def ajaxDelPurview(request):
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
                count = models.Purview.objects.filter(id__in=idsList).update(deletetime=datetime.now(),
                                                                             deleter=models.User.objects.filter(id=deleter)[0])

            scription = "成功删除 " + str(count) + " 条数据！"
            return JsonResponse({"result": "T", "scription": scription, "extendInfo": "你的extendInfo"})
    except Exception as e:
        # print(e)
        scription = "执行时发生异常！（Exception）：" + traceback.format_exc()
        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

# gridData
@csrf_exempt
def gridDataPurview(request):
    keywords = request.GET.get('keywords', '')
    grade = request.GET.get('grade', '')
    roleId = request.GET.get('roleId', '')
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
    if loginInfo == "":
        returnData = {"total": -1,"errorInfo": "登录超时，请重新登录！！！", "rows": []}
        return HttpResponse(json.dumps(returnData))

    records = models.Purview.objects.order_by(orderBy).filter(deletetime=None)
    if grade!="":
        records = records.filter(grade__lte = grade)
    if keywords != "":
        records = records.filter(
            Q(purname__contains=keywords) | Q(purcode__contains=keywords) | Q(memo__contains=keywords))

    total = records.count()
    results = records[start:end]

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

        #默认权限
        purV = "F"
        purA = "F"
        purE = "F"
        purD = "F"
        if roleId!="":
            rolePurviews = None
            if roleId == "0":
                rolePurviews = models.RolePur.objects.filter(deletetime=None, roleId=None, purcode=result.purcode,adder=adder)
            else:
                rolePurviews = models.RolePur.objects.filter(deletetime=None, roleId=roleId, purcode=result.purcode)
            for rolePur in rolePurviews:
                if rolePur.purview == "V":
                    purV = "T"
                if rolePur.purview == "A":
                    purA = "T"
                if rolePur.purview == "E":
                    purE = "T"
                if rolePur.purview == "D":
                    purD = "T"

        if userId!="":
            userPurviews = None
            if userId == "0":
                userPurviews = models.UserPur.objects.filter(deletetime=None, userId=None, purcode=result.purcode,adder=adder)
            else:
                userPurviews = models.UserPur.objects.filter(deletetime=None, userId=userId, purcode=result.purcode)
            for rolePur in userPurviews:
                if rolePur.purview == "V":
                    purV = "T"
                if rolePur.purview == "A":
                    purA = "T"
                if rolePur.purview == "E":
                    purE = "T"
                if rolePur.purview == "D":
                    purD = "T"

        returnData['rows'].append({
            "id": result.id,
            "purname": str(result.purname),
            "grade": str(result.grade),
            "gradeName": helpClass.systemGradeName[str(result.grade)],
            "purcode": str(result.purcode),
            "memo": str(result.memo),
            "sorts": str(result.sorts),
            "purV" : purV,
            "purA": purA,
            "purE": purE,
            "purD": purD,
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


# 排序
@csrf_exempt
def ajaxMoveSortsPurview(request):
    id = request.POST.get("id", "")
    moveType = request.POST.get("moveType", "")

    try:
        with transaction.atomic():
            if id != "" and moveType != "":
                curRecord = models.Purview.objects.get(id=id)
                if curRecord:
                    if moveType == "up":  # 上移
                        # 找到当前节点的上一个节点进行调换位置（排序位置）,如果找不到，说明当前已经是排在最上面的节点了，不做任何操作
                        preRecordQS = models.Purview.objects.filter(sorts__lt=curRecord.sorts).order_by("-sorts")
                        if preRecordQS:  # 找到上一个
                            preRecord = preRecordQS[0]
                            models.Purview.objects.filter(id=curRecord.id).update(sorts=preRecord.sorts)
                            models.Purview.objects.filter(id=preRecord.id).update(sorts=curRecord.sorts)
                            scription = "上移成功！"
                            return JsonResponse({"result": "T", "scription": scription, "extendInfo": "你的extendInfo"})
                        else:
                            scription = "上移失败，已在顶部！"
                            return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})
                    else:  # 下移
                        nextRecordQS = models.Purview.objects.filter(sorts__gt=curRecord.sorts).order_by("sorts")
                        if nextRecordQS:  # 找到下一个
                            nextRecord = nextRecordQS[0]
                            models.Purview.objects.filter(id=curRecord.id).update(sorts=nextRecord.sorts)
                            models.Purview.objects.filter(id=nextRecord.id).update(sorts=curRecord.sorts)
                            scription = "下移成功！"
                            return JsonResponse({"result": "T", "scription": scription, "extendInfo": "你的extendInfo"})
                        else:
                            scription = "下移失败，已在底部！"
                            return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})
    except Exception as e:
        # print(e)
        scription = "执行时发生异常！（Exception）：" + traceback.format_exc()
        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})



