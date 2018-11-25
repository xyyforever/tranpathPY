"""tranpathPY URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path,include
from system.views import views
from api_view import tempdic
from api_view import api_ware_view
urlpatterns = [
    # path('admin/', admin.site.urls),

    path('myTool/', include("system.urls.urlsExcel")),
    path('myTool/', include("system.urls.urlsCode")),
    path('menu/', include("system.urls.urlsMenu")),
    path('purview/', include("system.urls.urlsPurview")),
    path('syspara/', include("system.urls.urlsSyspara")),
    path('dicMainList/', include("system.urls.urlsDicMainList")),
    path('seller/', include("system.urls.urlsSeller")),
    path('dicMainListForSelect/', include("system.urls.urlsDicMainListForSelect")),
    path('role/', include("system.urls.urlsRole")),
    path('user/', include("system.urls.urlsUser")),
    path('informType/', include("system.urls.urlsInformType")),

    path('myTool/index/', views.myToolIndex),
    path('system/login/', views.login),
    path('system/ajaxLogin/', views.ajaxLogin),
    path('system/index/', views.index),
    path('system/changePsd/', views.changePsd),
    path('system/ajaxChangePsd/', views.ajaxChangePsd),

    path('common/setMenuFav/', views.setMenuFav),

    path('bindSeller/', include("basicInfo.urls.urlsBindSeller")),
    path('probrand/', include("basicInfo.urls.urlsProbrand")),
    path('dicWareclass/',include("basicInfo.urls.urlsDicWareclass")),
    path('dicArea/',include("basicInfo.urls.urlsDicArea")),

    path('api_ware_pro/', api_ware_view),

    path('index/test/', views.test),
    path('index/translateIndex/',tempdic.tlIndex),
    path('index/translate/', tempdic.translate),

]
