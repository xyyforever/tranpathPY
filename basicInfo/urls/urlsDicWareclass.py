from django.urls import path
from basicInfo.views import viewsDicWareclass

# 添加到urls.py
# path('dicWareclass/',include("basicInfo.urls.urlsDicWareclass")),

urlpatterns = [
    # path('admin/', admin.site.urls),

    path('index/', viewsDicWareclass.index),
    path('ajax_save_wareclass/', viewsDicWareclass.ajaxSaveDicWareclass),
    path('ajax_del_wareclass/', viewsDicWareclass.ajaxDelDicWareclass),
    path('get_pid_list/', viewsDicWareclass.ajaxMainMenuJson),
    path('getTreeJson/', viewsDicWareclass.getWareclassTreeList),

]
