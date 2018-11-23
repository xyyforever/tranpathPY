from django.urls import path
from system.views import viewsDicMainListForSelect

# 添加到urls.py
# path('dicMainListForSelect/',include("system.urlsDicMainListForSelect")),

urlpatterns = [
    # path('admin/', admin.site.urls),

    path('index/', viewsDicMainListForSelect.index),
    path('ajaxSaveDicMainListForSelect/', viewsDicMainListForSelect.ajaxSaveDicMainListForSelect),
    path('ajaxDelDicMainListForSelect/', viewsDicMainListForSelect.ajaxDelDicMainListForSelect),
    path('gridDataDicMainListForSelect/', viewsDicMainListForSelect.gridDataDicMainListForSelect),

    path('moveSortsDicMainListForSelect/', viewsDicMainListForSelect.ajaxMoveSortsDicMainListForSelect),

]
