# coding:utf-8
from django.conf import settings
from django.shortcuts import HttpResponseRedirect
from system import models

# 模板中使用的公共变量
def template(request):
    sysTitle = request.session.get('sysTitle', "管理系统")
    loginInfo = request.session.get('loginInfo',{})
    userId = loginInfo.get("userId",0)
    sellerId = loginInfo.get("sellerIdAll",0)
    menuList = request.session.get("menuList",[])
    favMenuList = request.session.get("favMenuList",[])
    purviewList = request.session.get('purviewList',[])#权限列表，list

    #print(menuList)

    menuParentId = request.GET.get("menuParentId","0")
    menuId = request.GET.get("menuId","0")

    menuMainName = ""
    menuSubName = ""
    if menuParentId !="0":
        try:
            menu = models.Menu.objects.get(id=menuParentId)
            if menu:
                menuMainName = menu.name
        except models.Menu.DoesNotExist:
            pass

    shortCutMenu = "false";
    if menuId !="0":
        try:
            menu = models.Menu.objects.get(id=menuId)
            if menu:
                menuSubName = menu.name
        except models.Menu.DoesNotExist:
            pass

        #快捷菜单是否已设置（true/false）
        objs = models.UserShortcutMenu.objects.filter(deletetime=None,userId=userId,menuId=menuId)
        if objs.count()>0:
            shortCutMenu = "true"

    pageInfo = {"menuParentId":int(menuParentId),"menuId":int(menuId),"curPath":request.path,"menuMainName":menuMainName,"menuSubName":menuSubName}

    return {'sysTitle': sysTitle,"loginInfo":loginInfo,"shortCutMenu":shortCutMenu,"menuList":menuList,"favMenuList":favMenuList,"pageInfo":pageInfo}