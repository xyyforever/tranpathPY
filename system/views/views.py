from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import traceback

from system import helpClass
from system.helpClass import login_required

import json
import datetime
from datetime import datetime

from system import models
from system.views import viewsMenu


# Create your views here.

def myToolIndex(request):
    return render(request, "system/myTool/index.html")


# 登录页
def login(request):
    # 判断session是否存在，如果存在则删除
    loginInfo = request.session.get('loginInfo', "")
    if loginInfo != "":
        del request.session["loginInfo"]
        del request.session["sysTitle"]
        del request.session["purviewList"]
        del request.session["menuList"]
        temp = request.session.get("favMenuList", "")
        if temp != "":
            del request.session["favMenuList"]

    sysTitle = helpClass.getSysparaValue(0, "sysTitle")

    return render(request, 'system/login/login.html', locals())
    # return HttpResponse("ABCD")


# 登录操作
@csrf_exempt
def ajaxLogin(request):
    # return JsonResponse(request.GET.get("data"))
    obj = json.loads(request.POST.get("data", ""))
    username = obj["username"]
    password = obj["password"]
    users = models.User.objects.filter(username=username).filter(password=password)

    # user = models.SysUser.objects.last()
    # print(user)
    # print(len(user))
    # print(type(user))
    # print(user[0].name + "XXXX")
    if users.count() == 0:
        return HttpResponse("用户名或密码错误！")
    else:
        user = users[0]
        loinInfo = {}
        loinInfo["userId"] = user.id
        loinInfo["username"] = user.username
        loinInfo["sellerId"] = user.sellerId
        loinInfo["sellerIdName"] = ""
        if user.sellerId > 0:
            loinInfo["sellerIdName"] = models.Seller.objects.filter(id=user.sellerId)[0].sellerName
        loinInfo["parentSellerId"] = user.parentSellerId
        loinInfo["sellerIdAll"] = 0
        if user.sellerId != 0:
            loinInfo["sellerIdAll"] = user.sellerId
        if user.parentSellerId != 0:
            loinInfo["sellerIdAll"] = user.parentSellerId

        if user.sellerId == 0 and user.parentSellerId == 0:
            loinInfo["grade"] = 3
        if user.sellerId != 0 and user.parentSellerId == 0:
            loinInfo["grade"] = 2
        if user.parentSellerId != 0:
            loinInfo["grade"] = 1

        request.session["loginInfo"] = loinInfo
        # request.session["sysTitle"] = "MyName"
        request.session["sysTitle"] = helpClass.getSysparaValue(loinInfo["sellerIdAll"], 'sysTitle')

        # 读取权限
        # 1.读取登录用户角色中的权限
        purviewList = []
        userRoles = models.UserRole.objects.filter(userId=user.id, deletetime=None)
        if userRoles.count() > 0:
            for userRole in userRoles:
                rolePurs = models.RolePur.objects.filter(roleId=userRole.roleId, deletetime=None)
                if rolePurs.count() > 0:
                    for rolePur in rolePurs:
                        pur = rolePur.purview + rolePur.purcode
                        if pur not in purviewList:
                            purviewList.append(pur)
        # 2.读取登录用户的权限
        userPurs = models.UserPur.objects.filter(userId=user.id, deletetime=None)
        if userPurs.count() > 0:
            for userPur in userPurs:
                pur = userPur.purview + userPur.purcode
                if pur not in purviewList:
                    purviewList.append(pur)

        request.session[
            "purviewList"] = purviewList  # ['A0001','A0002','A0003','A0004','A0005','A0006','A0007','A0008','A0009','A0010','A0011','A0012','D0001','D0002','D0003','D0004','D0005','D0006','D0007','D0008','D0009','D0010','D0011','D0012','E0001','E0002','E0003','E0004','E0005','E0006','E0007','E0008','E0009','E0010','E0011','E0012','V0001','V0002','V0003','V0004','V0005','V0006','V0007','V0008','V0009','V0010','V0011','V0012']
        temp = viewsMenu.getMenuTreeList(user.id, "", "T")
        # print(temp)
        request.session["menuList"] = temp
        request.session["favMenuList"] = viewsMenu.getFavMenuList(user.id)

        return HttpResponse("T")


# 登录后首页
@login_required
def index(request):
    return render(request, "system/login/index.html")


# 修改密码页
def changePsd(request):
    # request.POST
    # request.GET
    # return HttpResponse("Hello World!")
    # return render(request,"index.html")
    return render(request, "system/login/changePsd.html")


# 提交修改密码
# @csrf_exempt
def ajaxChangePsd(request):
    data = request.POST
    try:
        with transaction.atomic():
            if data != "":
                loginInfo = request.session.get('loginInfo', "")
                if loginInfo == "":
                    scription = "登录超时！"
                    return JsonResponse({"result": "F", "scription": scription, "extendInfo": "请重新登录"})

                adder = loginInfo["userId"]
                sellerId = loginInfo["sellerIdAll"]
                oldPassword = data["oldPassword"]
                newPassword = data["newPassword"]
                user = models.User.objects.get(id=adder)
                if user:
                    if user.password == oldPassword:
                        models.User.objects.filter(id=adder).update(password=newPassword, updatetime=datetime.now(),
                                                                    updater=adder)
                        scription = "修改密码成功！"
                        return JsonResponse({"result": "T", "scription": scription, "extendInfo": "你的extendInfo"})
                    else:
                        scription = "原密码错误，操作失败！"
                        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})
                else:
                    scription = "没有找到用户信息，操作失败！"
                    return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})


    except Exception as e:
        # print(e)
        traceback.print_exc()
        scription = "执行时发生异常！（Exception）：" + traceback.format_exc()
        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})


# 设置或取消快捷菜单
@csrf_exempt
def setMenuFav(request):
    menuId = request.POST.get("menuId", "")
    setOrCancel = request.POST.get("setOrCancel", "")
    if menuId != "" and setOrCancel != "":
        loginInfo = request.session.get('loginInfo', "")
        adder = loginInfo["userId"]
        sellerId = loginInfo["sellerIdAll"]

        if setOrCancel == "set":  # 设置快捷菜单
            objs = models.UserShortcutMenu.objects.filter(deletetime=None, userId=adder, menuId=menuId)
            if objs.count() == 0:
                obj = models.UserShortcutMenu.objects.create()
                obj.userId = models.User.objects.get(id=adder)
                obj.menuId = models.Menu.objects.get(id=menuId)
                obj.adder = models.User.objects.get(id=adder)
                obj.save()

            scription = "设置快捷菜单成功！"
            return JsonResponse({"result": "T", "scription": scription, "extendInfo": "你的extendInfo"})
        else:  # 取消快捷菜单
            models.UserShortcutMenu.objects.filter(deletetime=None, userId=adder, menuId=menuId).update(
                deletetime=datetime.now(), deleter=models.User.objects.filter(id=adder)[0])

            scription = "取消快捷菜单成功！"
            return JsonResponse({"result": "T", "scription": scription, "extendInfo": "你的extendInfo"})
    else:
        scription = "参数错误，操作失败！"
        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})


def test(request):
    exclude_fields = ('user', 'add_time')
    params = [f for f in models.User._meta.fields if f.name not in exclude_fields]
    print(params)
    for msg in params:
        print(msg.name, msg.help_text)

    return JsonResponse({"result": "test over!"})
