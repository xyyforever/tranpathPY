from django.urls import path
from basicInfo.views import viewsBindSeller

# 添加到urls.py
# path('bindSeller/',include("basicInfo.urlsBindSeller")),

urlpatterns = [
    # path('admin/', admin.site.urls),

    path('index/', viewsBindSeller.index),
    path('ajaxSaveBindSeller/', viewsBindSeller.ajaxSaveBindSeller),
    path('ajaxDelBindSeller/', viewsBindSeller.ajaxDelBindSeller),
    path('gridDataBindSeller/', viewsBindSeller.gridDataBindSeller),

]
