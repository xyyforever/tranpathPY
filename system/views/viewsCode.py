from django.shortcuts import render
from django.shortcuts import HttpResponse

import os
import json
import xlrd
import xlwt
import xlutils
import datetime
import random
import time

from system import  models


def code(request):

    purviewCode = request.POST.get("purviewCode","-1")
    if purviewCode == "-1":
        hasPurview = "#"
    else:
        hasPurview = ""

    folder = os.path.abspath(os.path.join(os.getcwd(), ""))+"/static/dbDesign"
    #print(folder)
    sheetName = ""
    L = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if os.path.splitext(file)[1] == '.xls' or os.path.splitext(file)[1] == '.xlsx':
                #L.append(os.path.join(file))
                fileFullPath = os.path.join(root,file)
                workbook = xlrd.open_workbook(fileFullPath)#打开execel
                sheetNames = workbook.sheet_names()
                #print(sheetNames)
                for sheet in sheetNames:
                    L.append({
                        "id": sheet + "|"+file,
                        "text": sheet + "["+file+"]",
                    })


    hasSorts = "F"#是否有sorts字段
    hasSellerId = ""#是否有sellerId字段(判断唯一值时使用)
    updateFieldsStr = ""#用户更新字段列表
    keywordsSearchStr = ""#keywords查询自动拼装（字符串型数据）
    fieldList = []
    jsValidate_rules = "rules:{     //配置验证规则，key就是被验证的dom对象，value就是调用验证的方法(也是json格式)\n"  # 表单验证规则
    jsValidate_messages = "messages:{\n"#表单验证提示
    js_init = ""#初始化dom对象，如select的option
    tableNameFull = request.POST.get("tableNameFull","")
    tableNameChinese = ""#表的中文名（如：菜单，用户，权限）
    if tableNameFull != "":
        sheetName,tableNameChinese,file = tableNameFull.split("|")
        #print(file)
        #print(sheetName)
        fileFullPath = os.path.join(folder, file)
        print(fileFullPath)
        workbook = xlrd.open_workbook(fileFullPath)  # 打开execel
        sheetNames = workbook.sheet_names()
        sheet = workbook.sheet_by_name(sheetName+"|"+tableNameChinese)
        rowsCount = sheet.nrows
        #colsCount = sheet.ncols
        for i in range(1, rowsCount):
            rows = sheet.row_values(i)  # 单行数据
            fieldName = rows[0]  #字段名
            fieldDataType = rows[1]  #字段数据类型
            fieldLength = rows[2]  #字段长度
            fieldForeignTable = rows[3]  #外键表名
            fieldAllowEmpty = rows[4]  #允许空
            fieldDefault = rows[5]  #默认值
            fieldMemo = rows[6]  #字段说明
            fieldDjangoExtend = rows[7]  #django额外属性
            fieldIfForm = rows[8]  #是否表单填写
            fieldIfShowInTable = rows[9]  #表单显示字段标题
            fieldTitle = rows[10]  #表单显示字段标题
            fieldMust = rows[11]  #是否必填
            fieldExtendLimit = rows[12]  #额外限制
            fieldInputType = rows[13]  #输入类型
            fieldIfMulti = rows[14]  #是否多值
            fieldUnique = rows[15]  #是否唯一
            fieldDataForSelect = rows[16]  #可选数据

            if fieldName == "sorts":
                hasSorts = "T"

            if fieldName == "sellerId":
                hasSellerId = "T"


            if fieldIfForm == "T":
                if updateFieldsStr == "":
                    updateFieldsStr = fieldName +"="+ fieldName
                else:
                    updateFieldsStr += "," + fieldName + "=" + fieldName

            #Q(purname__contains=keywords) | Q(purcode__contains=keywords)
            if fieldDataType == "CharField":
                if keywordsSearchStr == "":
                    keywordsSearchStr = "Q("+fieldName +"__contains=keywords)"
                else:
                    keywordsSearchStr += " | " + "Q("+fieldName +"__contains=keywords)"


            dataForSelect = ""
            if fieldDataForSelect != "":
                tempJson = json.loads(fieldDataForSelect)
                dataForSelect = str(tempJson.get("data","")).replace("'","\"")

            ac = ""
            if fieldInputType in ["select"]:
                ac = "选择"
            elif fieldInputType in ["text","textarea","password"]:
                ac = "输入"
            else:
                ac = "设置"

            if fieldMust == "T":
                if jsValidate_messages != "messages:{\n":
                    jsValidate_rules += ",\n"

                jsValidate_rules += "\t" + fieldName + ":{\n"
                jsValidate_rules += "\t\trequired:true  //必填。如果验证方法不需要参数，则配置为true\n"
                jsValidate_rules += "\t}"


                if jsValidate_messages != "messages:{\n":
                    jsValidate_messages += ",\n"

                jsValidate_messages += "\t" + fieldName + ":{\n"
                jsValidate_messages += "\t\trequired:\"请" + ac + fieldTitle + "！\"\n"
                jsValidate_messages += "\t}"


#{"data":[{"id":"3","text":"系统级"},{"id":"2","text":"商家级"},{"id":"1","text":"客服级"}]}

            fieldMemoStr = "verbose_name='"
            if (fieldTitle == ""):
                fieldMemoStr += fieldMemo
            else:
                fieldMemoStr += fieldTitle
            fieldMemoStr += "'"
            if (fieldLength !=""):
                fieldMemoStr += ",max_length="
                fieldMemoStr += str(int(fieldLength))
            if (fieldAllowEmpty == "T"):
                fieldMemoStr += ",null=True"
            if (fieldForeignTable != ""):
                fieldMemoStr = fieldForeignTable + ",related_name=\""+sheetName+"_"+fieldName+"\",on_delete=models.SET_NULL" + "," + fieldMemoStr
            if (fieldDjangoExtend != ""):
                fieldMemoStr += "," + fieldDjangoExtend
            if dataForSelect!="":
                fieldMemoStr += ",help_text='{\"data\":" + dataForSelect +"'"
            else:
                fieldMemoStr += ",help_text=''"

            fieldInputStr = ""
            if fieldInputType == "text":
                fieldInputStr = "<input type='text' id='" + fieldName + "' name='" + fieldName + "' class='form-control input-width-large'>"
            elif fieldInputType == "textarea":
                fieldInputStr = "<textarea id='" + fieldName + "' name='" + fieldName + "' rows=5 class='form-control input-width-large'></textarea>"
            elif fieldInputType == "password":
                fieldInputStr = "<input type='password' id='" + fieldName + "' name='" + fieldName + "' class='form-control input-width-large'>"
            elif fieldInputType == "select":
                fieldInputStr = "<select id='" + fieldName + "' name='" + fieldName + "' class='form-control input-width-large'></select>"

                js_init += "$(\"#" + fieldName + "\").select2({\n"
                js_init += "\tplaceholder:\"请选择\",\n"
                js_init += "\topenOnEnter:false,\n"
                js_init += "\tminimumResultsForSearch: -1,\n"
                if (dataForSelect!=""):
                    js_init += "\tdata:" + dataForSelect + "\n"
                else:
                    js_init += "\tdata:[]\n"
                js_init += "});\n"
                js_init += "$(\"#" + fieldName + "\").val('').trigger('change');\n\n"

            elif fieldInputType == "radio" or fieldInputType == "checkbox":
                #print(fieldDataForSelect)
                if fieldDataForSelect != "":
                    obj = json.loads(fieldDataForSelect)
                    i = 0
                    for o in obj["data"]:
                        checked = ""
                        #print(fieldDefault+"-"+o["id"])
                        if o["id"] == fieldDefault:
                            checked = "checked"
                        fieldInputStr += "<label class='radio-inline'>\n"
                        fieldInputStr += "\t\t\t\t\t<input type='" + fieldInputType + "' class='' id='" + fieldName+ str(i) + "' name='" + fieldName + "' value='" + o["id"] + "' " + checked + ">"
                        fieldInputStr += o["text"] + "\n"
                        fieldInputStr += "\t\t\t\t</label>"
                        i += 1
                else:
                    fieldInputStr = "<label class='radio-inline'>\n"
                    fieldInputStr += "\t\t\t\t\t<input type='" + fieldInputType + "' class='' id='" + fieldName + "' name='"  + fieldName + "' value='' checked>"
                    fieldInputStr += "选项一\n"
                    fieldInputStr += "\t\t\t\t</label>"
            elif fieldInputType == "datetime":
                fieldInputStr = "<input type='text' value='' id='" + fieldName + "' name='" + fieldName + "' data-date-format='yyyy-mm-dd' class='form-control input-width-small'>"

                if js_init == "":
                    js_init += "\n"
                js_init += "$(\"#" + fieldName + "\").datetimepicker({\n"
                js_init += "\tcontainer:'#modalAdd .modal-content',\n"
                js_init += "\tautoclose:true,\n"
                js_init += "\tlanguage:'zh-CN',\n"
                js_init += "\ttodayHighlight:true,\n"
                js_init += "\ttodayBtn:true,\n"
                js_init += "\tminView:2\n"
                js_init += "});\n"
            elif fieldInputType == "date":
                fieldInputStr = "<input type='text' value='' id='" + fieldName + "' name='" + fieldName + "' data-date-format='yyyy-mm-dd' class='form-control input-width-small'>"
                if js_init == "":
                    js_init += "\n"
                js_init += "$(\"#" + fieldName + "\").datetimepicker({\n"
                js_init += "\tcontainer:'#modalAdd .modal-content',\n"
                js_init += "\tautoclose:true,\n"
                js_init += "\tlanguage:'zh-CN',\n"
                js_init += "\ttodayHighlight:true,\n"
                js_init += "\ttodayBtn:true,\n"
                js_init += "\tminView:2\n"
                js_init += "});\n"
            elif fieldInputType == "time":
                fieldInputStr = "<input type='text' value='' id='" + fieldName + "' name='" + fieldName + "' data-date-format='yyyy-mm-dd' class='form-control input-width-small'>"
                if js_init == "":
                    js_init += "\n"
                js_init += "$(\"#" + fieldName + "\").datetimepicker({\n"
                js_init += "\tcontainer:'#modalAdd .modal-content',\n"
                js_init += "\tautoclose:true,\n"
                js_init += "\tlanguage:'zh-CN',\n"
                js_init += "\ttodayHighlight:false,\n"
                js_init += "\ttodayBtn:false,\n"
                js_init += "\tstartView: 1,\n"
                js_init += "\tminView: 0,\n"
                js_init += "\tmaxView: 1,\n"
                js_init += "\tforceParse: 0\n"
                js_init += "});\n"
            else:
                fieldInputStr = fieldName


            fieldList.append({
                "fieldName": fieldName,
                "fieldDataType": fieldDataType,
                "fieldLength": fieldLength,
                "fieldForeignTable": fieldForeignTable,
                "fieldAllowEmpty": fieldAllowEmpty,
                "fieldDefault": fieldDefault,
                "fieldMemo": fieldMemo,
                "fieldDjangoExtend": fieldDjangoExtend,
                "fieldIfForm": fieldIfForm,
                "fieldIfShowInTable": fieldIfShowInTable,
                "fieldTitle": fieldTitle,
                "fieldMust": fieldMust,
                "fieldExtendLimit": fieldExtendLimit,
                "fieldInputType": fieldInputType,
                "fieldIfMulti": fieldIfMulti,
                "fieldUnique": fieldUnique,
                "fieldDataForSelect": fieldDataForSelect,
                "fieldMemoStr": fieldMemoStr,
                "fieldInputStr": fieldInputStr,
            })

        jsValidate_rules += "\n},"
        jsValidate_messages += "\n},"

    #print(L)
    #return render(request, 'system/myTool/code.html', {"data": L})
    nameSpace,extend = file.split(".")
    #hasSorts = "F"  # 是否有sorts字段
    #hasSellerId = "F"  # 是否有sellerId字段
    #updateFieldsStr = ""  # 用户更新字段列表
    #keywordsSearchStr = ""#keywords查询自动拼装（字符串型数据）

    codeLeftTag = "{"
    codeRightTag = "}"

    objName = ""
    if (sheetName!=""):
        objName = sheetName[0].upper() + sheetName[1:]

    strings = {"tableName":sheetName,"tableNameChinese":tableNameChinese,"objName": objName,
               "nameSpace":nameSpace,"now":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
               "hasSorts":hasSorts,"hasSellerId":hasSellerId,"hasPurview":hasPurview,
               "updateFieldsStr":updateFieldsStr,"keywordsSearchStr":keywordsSearchStr,"codeLeftTag":codeLeftTag,"codeRightTag":codeRightTag}

    purviewQS = models.Purview.objects.filter(deletetime=None).order_by("sorts")
    purviewList = []
    purviewList.append({
        "id": "-1",
        "text": "不设置权限"
    })
    for purview in purviewQS:
        purviewList.append({
            "id":purview.purcode,
            "text": purview.purname+"("+purview.purcode+")"
        })

    return render(request, 'system/myTool/code.html', {"data":json.dumps(L), "tableNameFull":tableNameFull, "purviewList":json.dumps(purviewList), "purviewCode":purviewCode, "strings":strings, "fieldList":fieldList, "jsValidate_rules":jsValidate_rules, "jsValidate_messages":jsValidate_messages, "js_init":js_init})
