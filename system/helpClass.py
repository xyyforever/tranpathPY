import datetime
import json
from datetime import date
from django.db.models import Q
from django.shortcuts import redirect
from system import models

systemGradeName = {"3": "系统级", "2": "商家级", "1": "客服级"}

#检查是否登录
def login_required(view_func):
    '''检查用户是否登陆'''
    def wrapper(request):
        if request.session.get('loginInfo'):
            return view_func(request)
        else:
            return redirect('/system/login/')
    return wrapper


# 格式化日期
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        return json.JSONEncoder.default(self, obj)


# 获取用户列表供选择返回list([])
# condtion 查询条件，参数可变
def getUserForSelect(**condtion):
    orderBy = "-id"
    users = models.User.objects.order_by(orderBy).filter(deletetime=None)
    parentSellerId = condtion.get("parentSellerId", "")  # 返回指定键的值，如果值不在字典中返回default值#condtion["parentSellerId"]
    if (parentSellerId != ""):
        users = users.filter(parentSellerId=parentSellerId)
    userList = []
    for user in users:
        userList.append({
            "recordId": user.id,
            "id": user.id,
            "text": user.username
        })
    return userList


# 获取系统配置可选项
# sellerId:商家ID
# dicTag:选项标识
def getDicMainListForSelect(sellerId, dicTag):
    dicMainListForSelectList = []
    orderBy = "sorts"
    dicMainList = models.DicMainList.objects.get(dicTag=dicTag)
    if dicMainList:
        dicMainListForSelects = models.DicMainListForSelect.objects.order_by(orderBy).filter(
            dicMainListId=dicMainList.id, deletetime=None)
        if sellerId == 0:
            dicMainListForSelects = dicMainListForSelects.filter(sellerId=None)
        else:
            dicMainListForSelects = dicMainListForSelects.filter(Q(sellerId=sellerId) | Q(sellerId=None))

        i = 0
        for dicMainListForSelect in dicMainListForSelects:
            dicMainListForSelectList.append({
                "recordSn": i,
                "recordId": dicMainListForSelect.id,
                "id": dicMainListForSelect.valueForSelect,
                "text": dicMainListForSelect.textForSelect
            })
            i = i + 1
    else:
        dicMainListForSelectList.append({
            "recordId": "",
            "id": "",
            "text": "参数标识无效"
        })
    return dicMainListForSelectList


# 获取系统配置单值参数值
def getSysparaValue(sellerId, paraTag):
    if sellerId > 0:
        sysparaId = 0
        objs = models.Syspara.objects.filter(deletetime=None, paraTag=paraTag)
        if objs.count() > 0:
            sysparaId = objs[0].id

        if sysparaId > 0:
            objs = models.SysparaForSeller.objects.filter(deletetime=None, sysparaId=sysparaId, sellerId=sellerId)
            if objs.count() > 0:
                return objs[0].paraValue
            else:
                return "商家未配置参数（" + paraTag + "），联系开发人员"
        else:
            return "没有找到参数（" + paraTag + "）"
    else:
        objs = models.Syspara.objects.filter(deletetime=None, paraTag=paraTag)
        if objs.count() > 0:
            return objs[0].paraValue
        else:
            return "没有找到参数（" + paraTag + "），联系开发人员"


# 记录系统日志
def addSysLog(jsonObj):
    # {"sellerId":"sellerId","weiXinAppId":"weiXinAppId","openid":"openid","title":"title","info":"info","listsnType":"listsnType","listsn":"listsn","tableName":"tableName","tableId":"tableId","memo":"memo","adder":"adder"}
    # jsonObj = json.loads(jsonStr)
    obj = models.SysLog.objects.create()
    if jsonObj["sellerId"] != "":
        obj.sellerId = models.Seller.objects.filter(id=jsonObj["sellerId"])[0]
    obj.weiXinAppId = jsonObj["weiXinAppId"]
    obj.openid = jsonObj["openid"]
    obj.title = jsonObj["title"]
    obj.info = jsonObj["info"]
    obj.listsnType = jsonObj["listsnType"]
    obj.listsn = jsonObj["listsn"]
    obj.tableName = jsonObj["tableName"]
    obj.tableId = jsonObj["tableId"]
    obj.memo = jsonObj["memo"]
    if jsonObj["adder"] != "":
        obj.adder = models.User.objects.filter(id=jsonObj["adder"])[0]
    obj.save()


# 格式化字符串
def formatStr(obj):
    obj = str(obj)
    if obj == "None":
        obj = ""
    return obj


# 处理特殊符号
def formatContent(content):
    if content is None:
        return ""
    else:
        string = ""
        for c in content:
            if c == '"':
                string += '\\\"'
            elif c == "'":
                string += "\\\'"
            elif c == "\\":
                string += "\\\\"
            else:
                string += c
        return string
