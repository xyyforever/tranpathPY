from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.db import connection


import os
import json
import xlrd
import xlwt
import xlutils
import datetime
import random
import time
from system import models


#返回文件扩展名
def file_extension(path):
    return os.path.splitext(path)[1]

#执行sql返回影响行数或记录数
def executeSql(sqlStr):
    with connection.cursor() as cursor:
        cursor.execute(sqlStr)
        row = cursor.fetchone()
    return row



def excel(request):
    return render(request, 'system/myTool/excel.html')



@csrf_exempt
def ajaxUpload(request):
    if request.method == "POST":  # 请求方法为POST时，进行处理
        myFile = request.FILES.get("file", None)  # 获取上传的文件，如果没有文件，则默认为None
        tableNameStr =request.POST.get("tableName","")
        if tableNameStr!="":
            tableNameStr = "temp" + tableNameStr.capitalize()
        if not myFile:
            return JsonResponse({"result":"no files for upload!"})
        os.getcwd()
        preFolder = os.path.abspath(os.path.join(os.getcwd(), ""))

        filenameNew = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(0, 999999))#文件重命名
        filenameNew += file_extension(myFile.name)

        destination = open(os.path.join(preFolder+"/static/upload", filenameNew), 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()

        obj = models.Excel_import_file_main.objects.create()
        obj.filenameOriginal=myFile.name
        obj.filenameSaved = filenameNew
        obj.tableName = tableNameStr
        obj.save()

        return JsonResponse({"result":"upload over!"})

@csrf_exempt
def ajaxSetTableName(request):
    data = request.POST
    count = 0
    #print(data)
    if data!="":
        id = data["id"]
        tableName = data["tableName"]
        # jsonStr = str(data.dict()).replace('\'', '\"')
        # obj = json.loads(jsonStr)
        # id = obj["id"]
        # tableName = obj["tableName"]
        tableName = "temp" + tableName.capitalize()
        count = models.Excel_import_file_main.objects.filter(id=id).update(tableName=tableName)
        return HttpResponse(count)
    else:
        return HttpResponse("0")

#获取excel列表名（字段名）
@csrf_exempt
def ajaxGetTableFields(request):
    data = request.POST
    id = data["id"]
    if id!="":
        model = models.Excel_import_file_main.objects.filter(id=id)[0]
        if model:
            filenameSaved = model.filenameSaved
            folder = os.path.abspath(os.path.join(os.getcwd(), ""))
            filepathFull = folder + '/static/upload/' + filenameSaved
            workbook = xlrd.open_workbook(filepathFull)
            #sheet1Nname = workbook.sheet_names()[1]#根据下标获取sheet名称
            #根据sheet索引或者名称获取sheet内容，同时获取sheet名称、行数、列数
            #sheet2 = workbook.sheet_by_index(1)
            #sheet2 = workbook.sheet_by_name('Sheet2')
            #print(sheet2.name, sheet2.nrows, sheet2.ncols)
            #根据sheet名称获取整行和整列的值
            #sheet2 = workbook.sheet_by_name('Sheet2')
            #rows = sheet2.row_values(3)
            #cols = sheet2.col_values(2)
            #print rows
            #print cols
            #那么如果是在脚本中需要获取并显示单元格内容为日期类型的，可以先做一个判断。判断ctype是否等于3，如果等于3，则用时间格式处理：
            #if (sheet.cell(row, col).ctype == 3):
            #   date_value = xlrd.xldate_as_tuple(sheet.cell_value(row, col), book.datemode)
            #   date_tmp = date(*date_value[:3]).strftime('%Y/%m/%d')
            sheet = workbook.sheet_by_index(0)
            rows = sheet.row_values(0)#原始列名

            #数据类型
            colTypeNameList = ""
            colsCount = sheet.ncols
            i = 0
            d = {"0": "empty", "1": "string", "2": "number", "3": "date", "4": "boolean", "5": "error"}
            while i < colsCount:
                colType = str(sheet.cell(1, i).ctype)
                colTypeName = d[colType]
                #print(colType)
                #print(colTypeName)
                if colTypeNameList == "":
                    colTypeNameList = colTypeName
                else:
                    colTypeNameList += "|"+colTypeName
                i += 1

            return JsonResponse({"colsList":'|'.join(rows),"colTypeNameList":colTypeNameList})


#保存字段名
@csrf_exempt
def ajaxSaveTableFields(request):
    data = request.POST
    excelImportFileMainId = data["excelImportFileMainId"]
    fieldCount = data["fieldCount"]

    i = 0
    try:
        with transaction.atomic():
            while i < int(fieldCount):
                fieldNameNew = data["fieldNameNew" + str(i)]
                fieldNameOriginal = data["fieldNameOriginal" + str(i)]
                colTypeName = data["colTypeName" + str(i)]
                modelList = models.Excel_import_file_fields_name.objects.filter(
                    excelImportFileMainId=excelImportFileMainId, fieldSn=i)
                if modelList:
                    model = modelList[0]
                    models.Excel_import_file_fields_name.objects.filter(id=model.id).update(fieldNameNew=fieldNameNew)
                else:
                    obj = models.Excel_import_file_fields_name.objects.create()
                    obj.excelImportFileMainId = models.Excel_import_file_main.objects.filter(id=excelImportFileMainId)[0]
                    obj.fieldSn = i
                    obj.fieldNameOriginal = fieldNameOriginal
                    obj.fieldNameNew = fieldNameNew
                    obj.colType = colTypeName
                    obj.save()
                i += 1

            models.Excel_import_file_main.objects.filter(id=excelImportFileMainId).update(setFieldNameTime=datetime.datetime.now())

    except Exception as e:
        print(e)
        return HttpResponse("执行出现错误！")
    return HttpResponse("T")



def excel_import_file_main_list(request):
    keywords = request.GET.get('keywords','')

    #sortName = tableName & sortOrder = desc

    sortName = request.GET.get('sortName','')
    sortOrder = request.GET.get('sortOrder','')

    orderBy = "-id"
    if sortName != "":
        if sortOrder == "" or sortOrder == "asc":
            orderBy = sortName
        else:
            orderBy = "-"+sortName


    '''服务端分页时，前端需要传回：limit（每页需要显示的数据量），offset（分页时 数据的偏移量，即第几页）'''
    '''mysql 利用 limit语法 进行分页查询'''
    '''服务端分页时，需要返回：total（数据总量），rows（每行数据）  如： {"total": total, "rows": []}'''


    pageIndex = request.GET.get('pageIndex',1)
    pageSize  = request.GET.get('pageSize',20)
    #print(pageIndex)
    start = (int(pageIndex)-1) * int(pageSize)
    end = int(pageIndex) * int(pageSize)

    # 符合条件的总记录数
    if keywords == "":
        total = models.Excel_import_file_main.objects.all().count()
        results = models.Excel_import_file_main.objects.order_by(orderBy).all()[start:end]
    else:
        total = models.Excel_import_file_main.objects.filter(filenameOriginal__contains=keywords).count()
        results = models.Excel_import_file_main.objects.filter(filenameOriginal__contains=keywords).order_by(orderBy).all()[start:end]

    returnData = {"total": total, "rows": []}  #########非常重要############

    for result in results:
        #加载默认字段名列表
        fields = models.Excel_import_file_fields_name.objects.filter(excelImportFileMainId=result.id).order_by("fieldSn")
        defaultFieldsName = ""
        if fields:
            for f in fields:
                if (defaultFieldsName == ""):
                    defaultFieldsName += f.fieldNameNew
                else:
                    defaultFieldsName += "|"+f.fieldNameNew

        returnData['rows'].append({
            "id": result.id,
            "filenameOriginal": result.filenameOriginal,
            "filenameSaved": result.filenameSaved,
            "tableName": result.tableName,
            #"addTime":  time.strftime("%Y-%m-%d %H:%M:%S %Z", time.gmtime(result.addTime)),
            "addTime": str(result.addTime),
            "adder": result.adder,
            "setFieldNameTime": str(result.setFieldNameTime),
            "setFieldNamer": result.setFieldNamer,
            "importTime": str(result.importTime),
            "importer": result.importer,
            "defaultFieldsName":defaultFieldsName,
            #"PurchaseTime": time.strftime("%Y-%m-%d %H:%M:%S %Z", time.gmtime(results['purchasetime'])),
            # 将 时间戳 转换为 UTC时间
        })

    # 最后用dumps包装下，json.dumps({"rows": [{"gameorderid": 1}, {"gameorderid": 22}]})
    return HttpResponse(json.dumps(returnData))

#excel预览
def excel_import_file_preview(request):
    returnData = {}  #########非常重要############
    id = request.GET.get("id","")
    if id != "":
        model = models.Excel_import_file_main.objects.filter(id=id)[0]
        if model:
            filenameSaved = model.filenameSaved
            folder = os.path.abspath(os.path.join(os.getcwd(), ""))
            filepathFull = folder + '/static/upload/' + filenameSaved
            workbook = xlrd.open_workbook(filepathFull)
            # sheet1Nname = workbook.sheet_names()[1]#根据下标获取sheet名称
            # 根据sheet索引或者名称获取sheet内容，同时获取sheet名称、行数、列数
            # sheet2 = workbook.sheet_by_index(1)
            # sheet2 = workbook.sheet_by_name('Sheet2')
            # print(sheet2.name, sheet2.nrows, sheet2.ncols)
            # 根据sheet名称获取整行和整列的值
            # sheet2 = workbook.sheet_by_name('Sheet2')
            # rows = sheet2.row_values(3)
            # cols = sheet2.col_values(2)
            # print rows
            # print cols
            # 那么如果是在脚本中需要获取并显示单元格内容为日期类型的，可以先做一个判断。判断ctype是否等于3，如果等于3，则用时间格式处理：
            # if (sheet.cell(row, col).ctype == 3):
            #   date_value = xlrd.xldate_as_tuple(sheet.cell_value(row, col), book.datemode)
            #   date_tmp = date(*date_value[:3]).strftime('%Y/%m/%d')
            sheet = workbook.sheet_by_index(0)
            rows = sheet.row_values(0)  # 原始列名

            rowsCount = sheet.nrows
            colsCount = sheet.ncols

            #初始化字段名
            fields = models.Excel_import_file_fields_name.objects.filter(excelImportFileMainId=id).order_by("fieldSn")

            returnData = {"total": rowsCount-1, "rows": []}

            pageIndex = request.GET.get('pageIndex', 1)
            pageSize = request.GET.get('pageSize', 20)
            # print(pageIndex)
            start = (int(pageIndex) - 1) * int(pageSize)
            end = int(pageIndex) * int(pageSize)
            if end+1 <= rowsCount:
                end += 1
            else:
                end = rowsCount

            for i in range(start+1,end):
                tempDict = {}
                if fields:
                    for j,f in enumerate(fields):
                        value = str(sheet.cell(i, j).value)
                        if f.colType == "number":
                            value = round(float(value),2)
                        #print(i,j,value)
                        tempDict["field"+str(f.id)] = value

                #print("------------")

                returnData['rows'].append(tempDict)

    # 最后用dumps包装下，json.dumps({"rows": [{"gameorderid": 1}, {"gameorderid": 22}]})
    return HttpResponse(json.dumps(returnData))

@csrf_exempt
def excel_import_file_main_del(request):
    data = request.POST
    idsForDelete = data["idsForDelete"]

    try:
        with transaction.atomic():
            if idsForDelete != "":
                idsList = idsForDelete.split(",")
                for id in idsList:
                    model = models.Excel_import_file_main.objects.filter(id=id)[0]
                    if model:
                        tableName = model.tableName
                        filenameSaved = model.filenameSaved
                        #删除表
                        sql = "SELECT count(*) as acount FROM information_schema.TABLES WHERE table_name ='" + model.tableName + "'"
                        row = executeSql(sql)
                        if int(row[0]) > 0:
                            sql = "drop table " + tableName
                            executeSql(sql)
                        #删除文件
                        folder = os.path.abspath(os.path.join(os.getcwd(), ""))
                        filepathFull = folder + '/static/upload/' + filenameSaved
                        if os.path.exists(filepathFull):
                            os.remove(filepathFull)
                        #删除记录
                        models.Excel_import_file_main.objects.filter(id=id).delete()
    except Exception as e:
        print(e)
        return HttpResponse("执行出现错误！")

    return HttpResponse("T")

@csrf_exempt
def ajaxExcelImport(request):
    data = request.POST
    id = data["id"]
    try:
        with transaction.atomic():
            if id != "":
                model = models.Excel_import_file_main.objects.filter(id=id)[0]
                if model:
                    if model.importTime != None:
                        return HttpResponse("已导入！")
                    filenameSaved = model.filenameSaved
                    folder = os.path.abspath(os.path.join(os.getcwd(), ""))
                    filepathFull = folder + '/static/upload/' + filenameSaved
                    workbook = xlrd.open_workbook(filepathFull)
                    # sheet1Nname = workbook.sheet_names()[1]#根据下标获取sheet名称
                    # 根据sheet索引或者名称获取sheet内容，同时获取sheet名称、行数、列数
                    # sheet2 = workbook.sheet_by_index(1)
                    # sheet2 = workbook.sheet_by_name('Sheet2')
                    # print(sheet2.name, sheet2.nrows, sheet2.ncols)
                    # 根据sheet名称获取整行和整列的值
                    # sheet2 = workbook.sheet_by_name('Sheet2')
                    # rows = sheet2.row_values(3)
                    # cols = sheet2.col_values(2)
                    # print rows
                    # print cols
                    # 那么如果是在脚本中需要获取并显示单元格内容为日期类型的，可以先做一个判断。判断ctype是否等于3，如果等于3，则用时间格式处理：
                    # if (sheet.cell(row, col).ctype == 3):
                    #   date_value = xlrd.xldate_as_tuple(sheet.cell_value(row, col), book.datemode)
                    #   date_tmp = date(*date_value[:3]).strftime('%Y/%m/%d')
                    sheet = workbook.sheet_by_index(0)
                    rows = sheet.row_values(0)  # 原始列名

                    rowsCount = sheet.nrows
                    colsCount = sheet.ncols

                    # excel数据类型对应数据库字段类型
                    dataType = {"empty": "varchar(500)", "string": "varchar(500)", "number": "DOUBLE", "date": "datetime",
                                "boolean": "varchar(50)", "error": "varchar(500)"}

                    # 建表语句
                    sqlCreateTable = "CREATE TABLE " + model.tableName + "(id INT PRIMARY KEY AUTO_INCREMENT"

                    # 初始化字段名
                    fields = models.Excel_import_file_fields_name.objects.filter(excelImportFileMainId=id).order_by("fieldSn")
                    fieldList = []
                    if fields:
                        for f in fields:
                            fieldList.append(f.fieldNameNew)
                            if f.fieldNameNew != "":
                                sqlCreateTable += "," + f.fieldNameNew + " " + dataType[f.colType]
                    sqlCreateTable += ")"

                    sql = "SELECT count(*) as acount FROM information_schema.TABLES WHERE table_name ='" + model.tableName + "'"
                    row = executeSql(sql)
                    if int(row[0]) == 0:
                        print(sqlCreateTable)
                        executeSql(sqlCreateTable)

                    insertSql = ""

                    for i in range(1, rowsCount):
                        fieldsList = ""
                        valuesList = ""
                        if fields:
                            for j, f in enumerate(fields):
                                value = str(sheet.cell(i, j).value)
                                if f.colType == "number":
                                    if str(value) == '':
                                        value=0
                                    else:
                                        value = round(float(value), 2)
                                #print(i, j, value)
                                if fieldsList == "":
                                    fieldsList = f.fieldNameNew
                                    valuesList = "'"+str(value).replace("'","''")+"'"
                                else:
                                    fieldsList = fieldsList + "," + f.fieldNameNew
                                    valuesList = valuesList + ",'" + str(value).replace("'","''") + "'"
                        #if insertSql == "":
                            insertSql = "insert into " + model.tableName + " (" + fieldsList + ") values (" + valuesList + ")"
                            print(insertSql)
                            executeSql(insertSql)
                        #else:
                        #    insertSql += ";insert into " + model.tableName + " (" + fieldsList + ") values (" + valuesList + ")"

                        print("------------")
                    print(insertSql)
                    models.Excel_import_file_main.objects.filter(id=id).update(importTime=datetime.datetime.now())

    except Exception as e:
        print(e)
        return HttpResponse("执行出现错误！")

    return HttpResponse("T")


def excelPreviewImport(request):
    id = request.GET.get("id","")
    print('id', id)
    objList = models.Excel_import_file_main.objects.filter(id=id)
    if objList:
        obj = objList[0]

    objFieldList = models.Excel_import_file_fields_name.objects.filter(excelImportFileMainId=id)

    return render(request, "system/myTool/excelPreviewImport.html", {"obj":obj, "objFieldList":objFieldList})

@csrf_exempt
def ajaxExecSql(request):
    data = request.POST
    sqlStr = data["sqlStr"]
    if sqlStr != "":
        cursor = connection.cursor()
        cursor.execute(sqlStr)
        #row = cursor.fetchone()  # 返回结果行 或使用 #rows = cursor.fetchall()
        rows = cursor.fetchall()
        #print(rows)
        workbook = xlwt.Workbook(encoding='utf-8')
        booksheet = workbook.add_sheet('Sheet1', cell_overwrite_ok=True)
        workbook.add_sheet('Sheet2')

        for i,row in enumerate(rows):
            for j,col in enumerate(row):
                print(col)
                booksheet.write(i, j, str(col))
            #print("---------")

        folder = os.path.abspath(os.path.join(os.getcwd(), ""))
        filepathFull = folder + '/static/download/' + 'tempExcel.xls'
        workbook.save(filepathFull)

    return HttpResponse("tempExcel.xls")