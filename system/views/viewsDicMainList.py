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

purCodeMain = "0003"

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


#需要使用的特殊权限
    purview0012 = "0012"#(维护可选项)
    purview0012A = "F"
    purview0012E = "F"
    purview0012D = "F"

    if "A" + purview0012 in purviewList:
        purview0012A = "T"
    if "E" + purview0012 in purviewList:
        purview0012E = "T"
    if "D" + purview0012 in purviewList:
        purview0012D = "T"

    return render(request, "system/dicMainList/index.html", locals())


# 保存数据（添加或修改）
@csrf_exempt
def ajaxSaveDicMainList(request):
    data = request.POST
    # print(data)

    try:
        with transaction.atomic():
            if data != "":
                keywords = data["keywords"]
                dicName = data["dicName"]
                dicTag = data["dicTag"]
                allowSellerOp = data["allowSellerOp"]
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

                    model = models.DicMainList.objects.filter(dicName=dicName, deletetime=None)
                    if model:
                        scription = "字典名称已经存在（" + dicName + "）"
                        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})
                    model = models.DicMainList.objects.filter(dicTag=dicTag, deletetime=None)
                    if model:
                        scription = "字典标志已经存在（" + dicTag + "）"
                        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

                    sorts = 0
                    try:
                        model = models.DicMainList.objects.filter(deletetime=None).latest("sorts")
                        if model:
                            sorts = model.sorts + 1
                        else:
                            sorts = 1
                    except models.DicMainList.DoesNotExist:
                        sorts = 1

                    obj = models.DicMainList.objects.create()
                    obj.keywords = keywords
                    obj.dicName = dicName
                    obj.dicTag = dicTag
                    obj.allowSellerOp = allowSellerOp
                    obj.sorts = sorts
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

                    model = models.DicMainList.objects.exclude(id=id).filter(dicName=dicName, deletetime=None)
                    if model:
                        scription = "字典名称已经存在（" + dicName + "）"
                        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})
                    model = models.DicMainList.objects.exclude(id=id).filter(dicTag=dicTag, deletetime=None)
                    if model:
                        scription = "字典标志已经存在（" + dicTag + "）"
                        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})

                    count = models.DicMainList.objects.filter(id=id).update(keywords=keywords, dicName=dicName, dicTag=dicTag,
                        allowSellerOp=allowSellerOp, memo=memo,
                        updatetime=datetime.now(),
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
def ajaxDelDicMainList(request):

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
                count = models.DicMainList.objects.filter(id__in=idsList).update(deletetime=datetime.now(),
                                                                                 deleter=models.User.objects.filter(id=deleter)[
                                                                                     0])

            scription = "成功删除 " + str(count) + " 条数据！"
            return JsonResponse({"result": "T", "scription": scription, "extendInfo": "你的extendInfo"})
    except Exception as e:
        # print(e)
        scription = "执行时发生异常！（Exception）：" + traceback.format_exc()
        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})


# gridData
from basicInfo.helper import queryset_to_list
@csrf_exempt
def gridDataDicMainList(request):
    keywords = request.GET.get('keywords', '')
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
    adder = loginInfo["userId"]
    sellerId = loginInfo["sellerIdAll"]
    print(sellerId,type(sellerId))
    records = models.DicMainList.objects.order_by(orderBy).filter(deletetime=None)
    #如果是商家登录，则只显示允许商品修改的字典

    if sellerId>0:
        records = records.filter(allowSellerOp='T')

    if keywords != "":
        records = records.filter(
            Q(keywords__contains=keywords) | Q(dicName__contains=keywords) | Q(dicTag__contains=keywords) | Q(
                allowSellerOp__contains=keywords) | Q(memo__contains=keywords))

    total = records.count()
    results = records[start:end]
    list_results = queryset_to_list(results)
    returnData = {"total": total, "rows": list_results}  #########非常重要############

    # 最后用dumps包装下，json.dumps({"rows": [{"gameorderid": 1}, {"gameorderid": 22}]})
    return HttpResponse(json.dumps(returnData))


# 排序
@csrf_exempt
def ajaxMoveSortsDicMainList(request):
    id = request.POST.get("id", "")
    moveType = request.POST.get("moveType", "")

    try:
        with transaction.atomic():
            if id != "" and moveType != "":
                curRecord = models.DicMainList.objects.get(id=id)
                if curRecord:
                    if moveType == "up":  # 上移
                        # 找到当前节点的上一个节点进行调换位置（排序位置）,如果找不到，说明当前已经是排在最上面的节点了，不做任何操作
                        preRecordQS = models.DicMainList.objects.filter(sorts__lt=curRecord.sorts).order_by("-sorts")
                        if preRecordQS:  # 找到上一个
                            preRecord = preRecordQS[0]
                            models.DicMainList.objects.filter(id=curRecord.id).update(sorts=preRecord.sorts)
                            models.DicMainList.objects.filter(id=preRecord.id).update(sorts=curRecord.sorts)
                            scription = "上移成功！"
                            return JsonResponse({"result": "T", "scription": scription, "extendInfo": "你的extendInfo"})
                        else:
                            scription = "上移失败，已在顶部！"
                            return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})
                    else:  # 下移
                        nextRecordQS = models.DicMainList.objects.filter(sorts__gt=curRecord.sorts).order_by("sorts")
                        if nextRecordQS:  # 找到下一个
                            nextRecord = nextRecordQS[0]
                            models.DicMainList.objects.filter(id=curRecord.id).update(sorts=nextRecord.sorts)
                            models.DicMainList.objects.filter(id=nextRecord.id).update(sorts=curRecord.sorts)
                            scription = "下移成功！"
                            return JsonResponse({"result": "T", "scription": scription, "extendInfo": "你的extendInfo"})
                        else:
                            scription = "下移失败，已在底部！"
                            return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})
    except Exception as e:
        # print(e)
        scription = "执行时发生异常！（Exception）：" + traceback.format_exc()
        return JsonResponse({"result": "F", "scription": scription, "extendInfo": "你的extendInfo"})




#以下是额外的方法
#商家配置参数首页
def indexForSeller(request):
    # request.POST
    # request.GET
    # return HttpResponse("Hello World!")
    # return render(request,"index.html")
    loginInfo = request.session.get('loginInfo', "")
    if loginInfo == "":
        return render(request, "system/login/login.html", locals())

    purviewList = request.session.get('purviewList', [])  # 权限列表，list

    # 需要使用的特殊权限
    purview0012 = "0012"  # (维护可选项)
    purview0012A = "F"
    purview0012E = "F"
    purview0012D = "F"

    if "A" + purview0012 in purviewList:
        purview0012A = "T"
    if "E" + purview0012 in purviewList:
        purview0012E = "T"
    if "D" + purview0012 in purviewList:
        purview0012D = "T"

    return render(request, "system/dicMainList/indexForSeller.html", locals())