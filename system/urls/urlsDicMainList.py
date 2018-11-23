from django.urls import path
from system.views import viewsDicMainList

# 添加到urls.py
# path('dicMainList/',include("system.urlsDicMainList")),

urlpatterns = [
    # path('admin/', admin.site.urls),

    path('index/', viewsDicMainList.index),
    path('ajaxSaveDicMainList/', viewsDicMainList.ajaxSaveDicMainList),
    path('ajaxDelDicMainList/', viewsDicMainList.ajaxDelDicMainList),
    path('gridDataDicMainList/', viewsDicMainList.gridDataDicMainList),

    path('moveSortsDicMainList/', viewsDicMainList.ajaxMoveSortsDicMainList),

    path('indexForSeller/', viewsDicMainList.indexForSeller),
]
