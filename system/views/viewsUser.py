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

purCodeMain = "0006"


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

    loginInfo = request.session.get('loginInfo')
    adder = loginInfo["userId"]
    grade = loginInfo["grade"]
    sellerId = loginInfo["sellerIdAll"]
    gradeForOther = grade
    if grade != 3:
        gradeForOther = 1

    return render(request, "system/user/index.html", locals())


# 保存数据（添加或修改）
@csrf_exempt
def ajaxSaveUser(request):
    loginInfo = request.session.get('loginInfo', "")
    if loginInfo == "":
        scription = "操作失败（登录超时，请重新登录后重试！）"
        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

    data = request.POST
    # print(data)
    try:
        with transaction.atomic():
            if data != "":

                name = data["name"]
                username = data["username"]
                password = data["password"]
                status = data["status"]
                memo = data["memo"]
                menuIdList = data["menuIdList"]
                sellerId = data["sellerId"]

                # loginInfo = request.session.get('loginInfo', "")
                adder = loginInfo["userId"]
                grade = loginInfo["grade"]
                sellerIdAll = loginInfo["sellerIdAll"]

                id = data["id"]

                if id == "" or id == "0":
                    # 判断是否有操作权限
                    purviewList = request.session.get('purviewList', [])  # 权限列表，list
                    purCode = "A" + purCodeMain
                    if purCode not in purviewList:
                        scription = "对不起！您<span style='color:red'>没有权限</span>添加此数据（" + purCode + "）"
                        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

                    # 判断唯一性（是否存在）
                    model = models.User.objects.filter(username=username, parentSellerId=sellerIdAll, deletetime=None)
                    if model:
                        scription = "用户名已经存在（" + username + "）"
                        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

                    obj = models.User.objects.create()
                    obj.name = name
                    obj.username = username
                    obj.password = password
                    obj.status = status
                    obj.menuIdList = menuIdList
                    obj.memo = memo
                    obj.adder = adder
                    if sellerId != "":
                        obj.sellerId = models.Seller.objects.filter(id=sellerId)[0]

                    if grade == 3:
                        obj.grade = 3
                        obj.parentSellerId = 0
                    else:
                        obj.grade = 1
                        obj.parentSellerId = sellerIdAll

                    if sellerId != "":
                        obj.grade = 2
                        obj.parentSellerId = 0
                        models.Seller.objects.filter(id=sellerId).update(userId=obj)

                    count = obj.save()

                    # 处理权限
                    models.UserPur.objects.filter(deletetime=None, userId=None, adder=adder).update(userId=obj)
                    # 处理角色
                    models.UserRole.objects.filter(deletetime=None, userId=None, adder=adder).update(userId=obj)

                else:
                    # 判断是否有操作权限
                    purviewList = request.session.get('purviewList', [])  # 权限列表，list
                    purCode = "E" + purCodeMain
                    if purCode not in purviewList:
                        scription = "对不起！您<span style='color:red'>没有权限</span>修改此数据（" + purCode + "）"
                        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

                    # 判断唯一性（是否存在）
                    model = models.User.objects.exclude(id=id).filter(username=username, sellerId=sellerIdAll,
                                                                      deletetime=None)
                    if model:
                        scription = "用户名已经存在（" + username + "）"
                        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

                    if grade == 3:
                        grade = 3
                        parentSellerId = 0
                    else:
                        grade = 1
                        parentSellerId = sellerIdAll

                    if sellerId != "":
                        grade = 2
                        parentSellerId = 0

                    count = models.User.objects.filter(id=id).update(name=name, username=username, password=password,
                                                                     grade=grade, parentSellerId=parentSellerId,
                                                                     status=status, memo=memo,
                                                                     updatetime=datetime.now(), updater=adder)

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
def ajaxDelUser(request):
    loginInfo = request.session.get('loginInfo', "")
    if loginInfo == "":
        scription = "操作失败（登录超时，请重新登录后重试！）"
        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})
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
                # loginInfo = request.session.get('loginInfo', "")
                deleter = loginInfo["userId"]
                count = models.User.objects.filter(id__in=idsList).update(deletetime=datetime.now(), deleter=deleter)

            scription = "成功删除 " + str(count) + " 条数据！"
            return JsonResponse({"result": "T", "scription": scription, "extendInfo": "你的extendInfo"})
    except Exception as e:
        # print(e)
        traceback.print_exc()
        scription = "执行时发生异常！（Exception）：" + traceback.format_exc()
        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})


# gridData
@csrf_exempt
def gridDataUser(request):
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

    if grade == 3:
        records = models.User.objects.order_by(orderBy).filter(deletetime=None, grade__in=(2, 3))
    else:
        records = models.User.objects.order_by(orderBy).filter(deletetime=None, grade=1, parentSellerId=sellerId)

    if keywords != "":
        records = records.filter(
            Q(name__contains=keywords) | Q(username__contains=keywords) | Q(password__contains=keywords) | Q(
                menuIdList__contains=keywords) | Q(status__contains=keywords) | Q(memo__contains=keywords) | Q(
                uniqueCode__contains=keywords))

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
        if result.adder > 0:
            adder = result.adder
            adderName = models.User.objects.filter(id=result.adder)[0].username
        if result.updater > 0:
            updater = result.updater
            updaterName = models.User.objects.filter(id=result.updater)[0].username
        if result.deleter > 0:
            deleter = result.deleter
            deleterName = models.User.objects.filter(id=result.deleter)[0].username

        sellerIdName = ""
        if result.sellerId > 0:
            sellerIdName = models.Seller.objects.filter(id=result.sellerId)[0].sellerName

        returnData['rows'].append({
            "id": result.id,
            "grade": str(result.grade),
            "gradeName": helpClass.systemGradeName[str(result.grade)],
            "sellerId": str(result.sellerId),
            "sellerIdName": sellerIdName,
            "parentSellerId": str(result.parentSellerId),
            "name": str(result.name),
            "username": str(result.username),
            "password": str(result.password),
            "menuIdList": str(result.menuIdList),
            "status": str(result.status),
            "memo": str(result.memo),
            "uniqueCode": str(result.uniqueCode),
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


# 以下是额外的方法
# 设置或取消用户可访问的菜单
@csrf_exempt
def setUserMenu(request):
    loginInfo = request.session.get('loginInfo', "")
    if loginInfo == "":
        scription = "操作失败（登录超时，请重新登录后重试！）"
        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

    userId = request.POST.get("userId", "")
    menuPur = request.POST.get("menuPur", "")

    try:
        with transaction.atomic():
            if userId != "":
                count = models.User.objects.filter(id=userId).update(menuIdList=menuPur)
                scription = "设置成功！"
                return JsonResponse({"result": "T", "scription": scription, "extendInfo": "你的extendInfo"})
            else:
                scription = "设置失败！（参数错误:userId）"
                return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

    except Exception as e:
        # print(e)
        traceback.print_exc()
        scription = "执行时发生异常！（Exception）：" + traceback.format_exc()
        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})


# 设置（或取消）用户权限
@csrf_exempt
def setUserPur(request):
    loginInfo = request.session.get('loginInfo', "")
    if loginInfo == "":
        scription = "操作失败（登录超时，请重新登录后重试！）"
        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

    userId = request.POST.get("userId", "")
    purcode = request.POST.get("purcode", "")
    purList = request.POST.get("purList", "")
    opType = request.POST.get("opType", "")
    # print(data)
    try:
        with transaction.atomic():
            if userId != "":

                loginInfo = request.session.get('loginInfo', "")
                adder = loginInfo["userId"]
                sellerId = request.session.get('sellerId', "0")

                if purcode != "":
                    if opType == "set":  # 设置权限
                        if purList != "":
                            pList = purList.split(",")
                            for pur in pList:
                                results = models.UserPur.objects.filter(deletetime=None, userId=userId, purcode=purcode,
                                                                        purview=pur)
                                if userId == "0":
                                    results = results.filter(adder=models.User.objects.filter(id=adder)[0])
                                if (results.count() == 0):
                                    obj = models.UserPur.objects.create()
                                    if userId != "0":
                                        obj.userId = models.User.objects.filter(id=userId)[0]
                                    obj.purcode = purcode
                                    obj.purview = pur
                                    obj.adder = models.User.objects.filter(id=adder)[0]
                                    count = obj.save()

                        scription = "设置成功！"
                        return JsonResponse({"result": "T", "scription": scription, "extendInfo": "你的extendInfo"})
                    else:  # 取消权限
                        if purList != "":
                            pList = purList.split(",")
                            for pur in pList:
                                count = models.UserPur.objects.filter(userId=userId, purcode=purcode, purview=pur,
                                                                      deletetime=None).update(deletetime=datetime.now(),
                                                                                              deleter=
                                                                                              models.User.objects.filter(
                                                                                                  id=adder)[0])
                        scription = "取消成功！"
                        return JsonResponse({"result": "T", "scription": scription, "extendInfo": "你的extendInfo"})

                else:
                    scription = "操作失败！（参数错误:purcode）"
                    return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

            else:
                scription = "操作失败！（参数错误:userId）"
                return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})
    except Exception as e:
        # print(e)
        traceback.print_exc()
        scription = "执行时发生异常！（Exception）：" + traceback.format_exc()
        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})


# 设置或取消用户的角色
@csrf_exempt
def setUserRole(request):
    loginInfo = request.session.get('loginInfo', "")
    if loginInfo == "":
        scription = "操作失败（登录超时，请重新登录后重试！）"
        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

    userId = request.POST.get("userId", "")
    if userId == "":
        userId = "0"
    roleIds = request.POST.get("roleIds", "")
    opType = request.POST.get("opType", "")  # cancel:取消；set:设置

    try:
        with transaction.atomic():
            if userId != "":
                if roleIds != "":
                    # loginInfo = request.session.get('loginInfo', "")
                    adder = loginInfo["userId"]
                    sellerId = request.session.get('sellerId', "0")
                    if opType == "set":  # 设置
                        rList = roleIds.split(",")
                        for roleId in rList:
                            results = models.UserRole.objects.filter(deletetime=None, roleId=roleId)
                            if userId == "0":
                                results = results.filter(userId=None, adder=models.User.objects.filter(id=adder)[0])
                            else:
                                results = results.filter(userId=userId)
                            if (results.count() == 0):
                                obj = models.UserRole.objects.create()
                                if userId != "0":
                                    obj.userId = models.User.objects.filter(id=userId)[0]
                                obj.roleId = models.Role.objects.filter(id=roleId)[0]
                                obj.adder = models.User.objects.filter(id=adder)[0]
                                count = obj.save()

                        scription = "设置成功！"
                        return JsonResponse({"result": "T", "scription": scription, "extendInfo": "你的extendInfo"})
                    else:  # 取消
                        rList = roleIds.split(",")
                        if userId == "0":
                            count = models.UserRole.objects.filter(userId=None, roleId__in=rList).update(
                                deletetime=datetime.now(), deleter=models.User.objects.filter(id=adder)[0])
                        else:
                            count = models.UserRole.objects.filter(userId=userId, roleId__in=rList).update(
                                deletetime=datetime.now(), deleter=models.User.objects.filter(id=adder)[0])
                        scription = "取消成功！"
                        return JsonResponse({"result": "T", "scription": scription, "extendInfo": "你的extendInfo"})

                else:
                    scription = "操作失败！（参数错误:roleIds）"
                    return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})
            else:
                scription = "操作失败！（参数错误:userId）"
                return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

    except Exception as e:
        # print(e)
        traceback.print_exc()
        scription = "执行时发生异常！（Exception）：" + traceback.format_exc()
        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})


# 设置或取消用户单值参数
@csrf_exempt
def setUserPara(request):
    loginInfo = request.session.get('loginInfo', "")
    userId = request.POST.get("userId", "")
    if userId == "":
        userId = "0"
    print('user:', userId , type(userId))
    sysparaIds = request.POST.get("id_list", "")
    opType = request.POST.get("opType", "")  # F:取消；T:设置

    try:
        with transaction.atomic():
            if sysparaIds != "":
                # adder = loginInfo["userId"]
                # sellerId = request.session.get('sellerId', "0")
                if opType == "T":  # 设置
                    rList = sysparaIds.split(",")
                    models.UserPara.add_relations(int(userId), rList)
                    scription = "设置成功！"
                    return JsonResponse({"result": "T", "scription": scription, "extendInfo": "你的extendInfo"})
                else:  # 取消
                    rList = sysparaIds.split(",")
                    models.UserPara.del_relations(userId, rList)
                    scription = "取消成功！"
                    return JsonResponse({"result": "T", "scription": scription, "extendInfo": "你的extendInfo"})
            else:
                scription = "操作失败！（参数错误:sysparaIds）"
                return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})
    except Exception as e:
        # print(e)
        traceback.print_exc()
        scription = "执行时发生异常！（Exception）：" + traceback.format_exc()
        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

# 设置或取消用户字典参数
@csrf_exempt
def setUserDic(request):
    loginInfo = request.session.get('loginInfo', "")
    userId = request.POST.get("userId", "")
    print('userid:', userId ,type(userId))
    if userId == "":
        userId = "0"
    dic_Ids = request.POST.get("id_list", "")
    opType = request.POST.get("opType", "")  # F:取消；T:设置

    try:
        with transaction.atomic():
            if dic_Ids != "":
                # adder = loginInfo["userId"]
                # sellerId = request.session.get('sellerId', "0")
                if opType == "T":  # 设置
                    rList = dic_Ids.split(",")
                    models.User_dic.add_relations(int(userId), rList)
                    scription = "设置成功！"
                    return JsonResponse({"result": "T", "scription": scription, "extendInfo": "你的extendInfo"})
                else:  # 取消
                    rList = dic_Ids.split(",")
                    models.User_dic.del_relations(int(userId), rList)
                    scription = "取消成功！"
                    return JsonResponse({"result": "T", "scription": scription, "extendInfo": "你的extendInfo"})
            else:
                scription = "操作失败！（参数错误:sysparaIds）"
                return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})
    except Exception as e:
        # print(e)
        traceback.print_exc()
        scription = "执行时发生异常！（Exception）：" + traceback.format_exc()
        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})


# 设置或取消用户对应的商家
@csrf_exempt
def setUserSeller(request):
    loginInfo = request.session.get('loginInfo', "")
    if loginInfo == "":
        scription = "操作失败（登录超时，请重新登录后重试！）"
        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

    sellerIdLogin = loginInfo["sellerIdAll"]
    if sellerIdLogin == 0:
        userId = request.POST.get("userId", "")
        sellerId = request.POST.get("sellerId", "")
        try:
            with transaction.atomic():
                if sellerId == "":
                    user = models.User.objects.filter(id=userId)[0]
                    models.User.objects.filter(id=userId).update(sellerId=0, parentSellerId=0, grade=3)
                    if user.sellerId > 0:
                        models.Seller.objects.filter(id=user.sellerId).update(userId=None)
                        scription = "取消成功！"
                    else:
                        scription = ""
                    return JsonResponse({"result": "T", "scription": scription, "extendInfo": "你的extendInfo"})
                else:
                    user = models.User.objects.filter(id=userId)[0]
                    models.User.objects.filter(id=userId).update(sellerId=sellerId, parentSellerId=0, grade=2)
                    models.Seller.objects.filter(id=sellerId).update(userId=user)
                    if str(user.sellerId) != str(sellerId):
                        scription = "设置成功！"
                    else:
                        scription = ""
                    return JsonResponse({"result": "T", "scription": scription, "extendInfo": "你的extendInfo"})

        except Exception as e:
            # print(e)
            traceback.print_exc()
            scription = "执行时发生异常！（Exception）：" + traceback.format_exc()
            return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})
    else:
        scription = ""
        return JsonResponse({"result": "T", "scription": scription, "extendInfo": "你的extendInfo"})

