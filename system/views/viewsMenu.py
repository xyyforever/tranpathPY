from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from system import models
import json
from system import helpClass
from django.db import transaction
import traceback
from datetime import datetime
from system.helpClass import login_required


@login_required
def index(request):
    return render(request, "system/menu/index.html", locals())


def getMenuTreeList(userId, grade, ifshow):
    if userId == "":
        userId = 0
    else:
        userId = int(userId)

    menuIds = []
    if userId > 0:  # 获取用户的菜单权限（包括用户所在的角色）

        # 获取用户所有角色中的菜单Id
        userRoles = models.UserRole.objects.filter(deletetime=None, userId=userId)
        if userRoles:
            for userRole in userRoles:
                tempMenuIdStr = userRole.roleId.menuIdList
                if tempMenuIdStr != "" and tempMenuIdStr != None:
                    tempMenuIds = tempMenuIdStr.split(",")
                    menuIds.extend(tempMenuIds)

        # 获取用户的菜单权限
        user = models.User.objects.filter(id=userId)[0]
        if user.menuIdList != "" and user.menuIdList != None:
            tempMenuIds = user.menuIdList.split(",")
            menuIds.extend(tempMenuIds)

    mainMenuList = []

    parentMenus = models.Menu.objects.order_by("sorts").filter(parentId=0, deletetime=None)
    if ifshow == "T":
        parentMenus = parentMenus.filter(ifshow='T')
    if grade != "":
        parentMenus = parentMenus.filter(grade__lte=grade)

    if userId > 0:
        parentMenus = parentMenus.filter(id__in=menuIds)  # 仅返回允许访问的菜单

    for mainMenu in parentMenus:
        newDict = mainMenu.__dict__
        newDict.pop('_state')

        subMenus = models.Menu.objects.order_by("sorts").filter(parentId=mainMenu.id, deletetime=None)
        if ifshow == "T":
            subMenus.filter(ifshow='T')
        if grade != "":
            subMenus = subMenus.filter(grade__lte=grade)

        if userId > 0:
            subMenus = subMenus.filter(id__in=menuIds)  # 仅返回允许访问的菜单

        subList = []
        for subMenu in subMenus:
            newSubDict = subMenu.__dict__
            newSubDict.pop('_state')
            subList.append(json.loads(json.dumps(newSubDict, cls=helpClass.DateTimeEncoder, indent=4)))

        newDict["nodes"] = subList
        mainMenuList.append(json.loads(json.dumps(newDict, cls=helpClass.DateTimeEncoder, indent=4)))
    return mainMenuList


# gridData
@csrf_exempt
def getFavMenuList(userId):
    orderBy = "id"
    results = models.UserShortcutMenu.objects.order_by(orderBy).filter(deletetime=None, userId=userId)

    favMenuList = []

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

        parentIdName = ""
        if result.menuId.parentId > 0:
            parentIdName = models.Menu.objects.get(id=result.menuId.parentId).name

        favMenuList.append({
            "id": result.id,
            "menuId": result.menuId.id,
            "name": str(result.menuId.name),
            "grade": str(result.menuId.grade),
            "parentId": str(result.menuId.parentId),
            "parentIdName": parentIdName,
            "linkfile": str(result.menuId.linkfile),
            "paras": str(result.menuId.paras),
            "target": str(result.menuId.target),
            "iconShow": str(result.menuId.iconShow),
            "memo": str(result.menuId.memo),
            "ifshow": str(result.menuId.ifshow),
            "sorts": str(result.menuId.sorts),
            "addtime": str(result.menuId.addtime),
            "updatetime": str(result.menuId.updatetime),
            "deletetime": str(result.menuId.deletetime),
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
    return favMenuList


# ajax返回Json主菜单（提供下拉选择）
@csrf_exempt
def ajaxMainMenuJson(request):
    mainMenu = models.Menu.objects.filter(parentId=0, deletetime=None).order_by("sorts")
    newList = []
    newList.append({
        "id": "0",
        "text": "顶级菜单",
        "name": "顶级菜单"
    })
    if mainMenu:
        for menu in mainMenu:
            newList.append({
                "id": menu.id,
                "text": menu.name,
                "name": menu.name
            })
    # return JsonResponse(newList)
    # return HttpResponse(json.dumps(newList))
    return HttpResponse(json.dumps(newList))


# ajax返回Json树结构

# checkedIds:默认checked的记录Id列表（checkbox）
# disabledIds:默认disabled的记录Id列表
# expandedIds:默认expanded的记录Id列表
# selectedIds:默认selected的记录Id列表

@csrf_exempt
def ajaxMenuTreeJson(request):
    userId = request.POST.get("userId", "0")
    grade = request.POST.get("grade", "")
    ifshow = request.POST.get("ifshow", "")
    checkedIds = request.POST.get("checkedIds", "")
    disabledIds = request.POST.get("disabledIds", "")
    expandedIds = request.POST.get("expandedIds", "")
    selectedIds = request.POST.get("selectedIds", "")

    checkedIdsList = checkedIds.strip(',').split(',')
    disabledIdsList = disabledIds.strip(',').split(',')
    expandedIdsList = expandedIds.strip(',').split(',')
    selectedIdsList = selectedIds.strip(',').split(',')

    menuList = getMenuTreeList(userId, grade, ifshow)

    # 添加bootstrap-treeview要求的key
    for main in menuList:
        main["id"] = main["id"]
        main["pId"] = main["parentId"]
        main["text"] = main["name"]
        main["icon"] = ""
        main["selectedIcon"] = ""
        main["color"] = "#000000"
        main["backColor"] = "#FFFFFF"
        main["href"] = ""
        main["selectable"] = "true"
        stat = {}
        if str(main["id"]) in checkedIdsList:
            stat["checked"] = "true"
        else:
            stat["checked"] = "false"
        if str(main["id"]) in disabledIdsList:
            stat["disabled"] = "true"
        else:
            stat["disabled"] = "false"
        if str(main["id"]) in expandedIdsList or expandedIds == "":
            stat["expanded"] = "true"
        else:
            stat["expanded"] = "false"
        if str(main["id"]) in selectedIdsList:
            stat["selected"] = "true"
        else:
            stat["selected"] = "false"

        main["state"] = stat
        tag = []
        main["tags"] = tag

        for sub in main["nodes"]:
            sub["id"] = sub["id"]
            sub["pId"] = sub["parentId"]
            sub["text"] = sub["name"]
            sub["icon"] = ""
            sub["selectedIcon"] = ""
            sub["color"] = "#000000"
            sub["backColor"] = "#FFFFFF"
            sub["href"] = ""
            sub["selectable"] = "true"
            stat = {}
            if str(sub["id"]) in checkedIdsList:
                stat["checked"] = "true"
            else:
                stat["checked"] = "false"
            if str(sub["id"]) in disabledIdsList:
                stat["disabled"] = "true"
            else:
                stat["disabled"] = "false"
            if str(sub["id"]) in expandedIdsList or expandedIds == "":
                stat["expanded"] = "true"
            else:
                stat["expanded"] = "false"
            if str(sub["id"]) in selectedIdsList:
                stat["selected"] = "true"
            else:
                stat["selected"] = "false"
            sub["state"] = stat
            tag = []
            sub["tags"] = tag

    menuJson = json.dumps(menuList).replace("\"true\"", "true").replace("\"false\"", "false")
    # print(menuJson)
    return HttpResponse(menuJson)


# 保存菜单
@csrf_exempt
def ajaxSaveMenu(request):
    # {"name":"系统/用户","grade":"3","parentId":"","linkfile":"","paras":"","target":"","icon":"","memo":"","id":"","ifshow":"T"}
    data = request.POST
    count = 0
    scription = ""
    # print(data)
    try:
        with transaction.atomic():
            if data != "":
                id = data["id"]
                name = data["name"]
                grade = data["grade"]
                parentId = data["parentId"]
                linkfile = data["linkfile"]
                paras = data["paras"]
                target = data["target"]
                iconShow = data["iconShow"]
                memo = data["memo"]
                ifshow = data["ifshow"]

                if parentId == "":
                    parentId = "0"

                loginInfo = request.session.get('loginInfo', "")
                adder = loginInfo["userId"]

                if id == "":  # 添加
                    # 判断同名菜单是否存在
                    model = models.Menu.objects.filter(name=name, deletetime=None)
                    if model:
                        scription = "菜单名已经存在（" + name + "）"
                        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

                    sorts = 0
                    try:
                        model = models.Menu.objects.filter(parentId=parentId, deletetime=None).latest("sorts")
                        if model:
                            sorts = model.sorts + 1
                        else:
                            sorts = 1
                    except models.Menu.DoesNotExist:
                        sorts = 1

                    menuNew = models.Menu.objects.create()
                    menuNew.name = name
                    menuNew.grade = grade
                    menuNew.parentId = parentId
                    menuNew.linkfile = linkfile
                    menuNew.paras = paras
                    menuNew.target = target
                    menuNew.iconShow = iconShow
                    menuNew.memo = memo
                    menuNew.ifshow = ifshow
                    menuNew.sorts = sorts
                    menuNew.adder = models.User.objects.filter(id=adder)[0]

                    # = models.Menu.objects.filter(parentId=parentId).order_by("-sorts")

                    menuNew.save()
                    scription = "菜单新建成功！（" + name + "）"
                else:  # 更新
                    models.Menu.objects.filter(id=id).update(name=name, grade=grade, parentId=parentId,
                                                             linkfile=linkfile, paras=paras, target=target,
                                                             iconShow=iconShow, memo=memo, ifshow=ifshow,
                                                             updatetime=datetime.now(),
                                                             updater=models.User.objects.filter(id=adder)[0])
                    scription = "菜单修改成功！（" + name + "）"

                # print(model)
            return JsonResponse({"result": "T", "scription": scription, "extendInfo": "你的extendInfo"})
    except Exception as e:
        # print(e)
        scription = "执行时发生异常！（Exception）：" + traceback.format_exc()
        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

    # 菜单排序


# 移动
@csrf_exempt
def ajaxMoveSorts(request):
    id = request.POST.get("id", "")
    moveType = request.POST.get("moveType", "")
    try:
        with transaction.atomic():
            if id != "" and moveType != "":
                curMenu = models.Menu.objects.get(id=id)
                if curMenu:
                    if moveType == "up":  # 上移
                        # 找到当前节点的上一个节点进行调换位置（排序位置）,如果找不到，说明当前已经是排在最上面的节点了，不做任何操作
                        preMenuQS = models.Menu.objects.filter(parentId=curMenu.parentId,
                                                               sorts__lt=curMenu.sorts).order_by("-sorts")
                        if preMenuQS:  # 找到上一个
                            preMenu = preMenuQS[0]
                            models.Menu.objects.filter(id=curMenu.id).update(sorts=preMenu.sorts)
                            models.Menu.objects.filter(id=preMenu.id).update(sorts=curMenu.sorts)
                            return HttpResponse("T")
                        else:
                            return HttpResponse("N")
                    else:  # 下移
                        nextMenuQS = models.Menu.objects.filter(parentId=curMenu.parentId,
                                                                sorts__gt=curMenu.sorts).order_by("sorts")
                        if nextMenuQS:  # 找到下一个
                            nextMenu = nextMenuQS[0]
                            models.Menu.objects.filter(id=curMenu.id).update(sorts=nextMenu.sorts)
                            models.Menu.objects.filter(id=nextMenu.id).update(sorts=curMenu.sorts)
                            return HttpResponse("T")
                        else:
                            return HttpResponse("N")
    except Exception as e:
        # print(e)
        # scription = "执行时发生异常！（Exception）：" + traceback.format_exc()
        # return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})
        return HttpResponse("F")

    # 删除菜单


# 删除ß
@csrf_exempt
def ajaxDelMenu(request):
    try:
        with transaction.atomic():
            idsForDelete = request.POST.get("idsForDelete", "")
            if idsForDelete != "":
                idsList = idsForDelete.strip(',').split(',')
                loginInfo = request.session.get('loginInfo', "")
                deleter = loginInfo["userId"]
                models.Menu.objects.filter(id__in=idsList).update(deletetime=datetime.now(),
                                                                  deleter=models.User.objects.filter(id=deleter)[0])
                models.Menu.objects.filter(parentId__in=idsList).update(deletetime=datetime.now(),
                                                                        deleter=models.User.objects.filter(id=deleter)[
                                                                            0])

            return HttpResponse("T")

    except Exception as e:
        # print(e)
        # scription = "执行时发生异常！（Exception）：" + traceback.format_exc()
        # return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})
        return HttpResponse("F")
