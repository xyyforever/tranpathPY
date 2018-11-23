from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api_view.models import _mysql

def tlIndex(request):
    return render(request,"api_templates/transalate.html")

@csrf_exempt
def translate(request):
    data = request.POST.get("data","")
    tempArray = data.split("\n")
    returnStr = ""
    str = ""
    for t in tempArray:
        sql = 'select ch from tempTempdic where en = "%s"' %t
        print(sql)
        result = _mysql(sql)
        print(result)
        if result.__len__()>0:
            str = result[0][0]
        else:
            str = t

        if returnStr == "":
            returnStr = str
        else:
            returnStr = returnStr + "|" +str;


    return HttpResponse(returnStr)