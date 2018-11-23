from django.urls import path
from basicInfo.views import viewsDicArea

# 添加到urls.py
# path('dicArea/',include("basicInfo.urls.urlsDicArea")),

urlpatterns = [
    # path('admin/', admin.site.urls),

    path('index/', viewsDicArea.index),
    path('getTreeJson/', viewsDicArea.getAreaTreeList),
    path('save_dicarea/',viewsDicArea.ajaxSaveArea),
    path('get_pid_list/',viewsDicArea.ajaxMainMenuJson),
    path('ajaxDelDicArea/',viewsDicArea.ajaxDelArea)
]
