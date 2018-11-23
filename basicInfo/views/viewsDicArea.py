from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from basicInfo import models as basicinfo_models
from system import models as system_models
import json
from system import helpClass
from django.db import transaction
import traceback
from datetime import datetime

purCodeMain = "0015"


# 区域维护首页
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
    return render(request, "basicInfo/dicArea/index.html", locals())


# 获得tree数据
from basicInfo.helper import queryset_to_list


def getAreaTreeList(request):
    dic_areas = basicinfo_models.DicArea.objects.filter(deletetime=None).order_by("sorts")
    data_list = queryset_to_list(dic_areas)
    return HttpResponse(json.dumps(data_list))


# 获取父类数据
@csrf_exempt
def ajaxMainMenuJson(request):
    mainMenu = basicinfo_models.DicArea.objects.filter(deletetime=None).order_by("sorts")
    newList = []
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


# 保存
@csrf_exempt
def ajaxSaveArea(request):
    data = request.POST
    scription = ""
    print(data)
    try:
        with transaction.atomic():
            if data != "":
                id = data["id"]
                parentid = data["parentId"]
                name = data["name"]
                memo = data["memo"]

                if parentid == "":
                    parentid = 0
                else:
                    parentid = int(parentid)
                print(parentid)
                if id == "":  # 添加
                    # 判断同名区域是否存在
                    model = basicinfo_models.DicArea.objects.filter(name=name, deletetime=None)
                    if model:
                        scription = "区域名%s已经存在" % name
                        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo1"})

                    try:
                        model = basicinfo_models.DicArea.objects.filter(parentId=parentid, deletetime=None).latest(
                            "sorts")
                        if model:
                            sorts = model.sorts + 1
                        else:
                            sorts = 1
                    except basicinfo_models.DicArea.DoesNotExist:
                        sorts = 1

                    new_area = basicinfo_models.DicArea.objects.create()
                    new_area.name = name
                    new_area.parentId = parentid
                    new_area.memo = memo
                    new_area.sorts = sorts

                    new_area.save()
                    scription = "区域%s新建成功！" % name
                else:  # 更新
                    basicinfo_models.DicArea.objects.filter(id=id).update(name=name, parentId=parentid, memo=memo,
                                                                          updatetime=datetime.now())
                    scription = "区域%s修改成功！" % name

                # print(model)
            return JsonResponse({"result": "T", "scription": scription, "extendInfo": "你的extendInfo2"})
    except Exception as e:

        scription = "执行时发生异常！（Exception）：" + traceback.format_exc()
        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo3"})


# 删除
@csrf_exempt
def ajaxDelArea(request):
    try:
        with transaction.atomic():
            idsForDelete = request.POST.get("idsForDelete", "")
            if idsForDelete != "":
                idsList = idsForDelete.strip(',').split(',')
                loginInfo = request.session.get('loginInfo', "")
                deleter = loginInfo["userId"]
                basicinfo_models.DicArea.objects.filter(id__in=idsList).update(deletetime=datetime.now(), deleter=
                system_models.User.objects.filter(id=deleter)[0])
                basicinfo_models.DicArea.objects.filter(parentId__in=idsList).update(deletetime=datetime.now(), deleter=
                system_models.User.objects.filter(id=deleter)[0])

            return HttpResponse("T")

    except Exception as e:
        return HttpResponse("F")
