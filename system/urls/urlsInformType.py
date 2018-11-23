from django.urls import path
from system.views import viewsInformType

# 添加到urls.py
# path('informType/',include("system.urlsInformType")),

urlpatterns = [
    # path('admin/', admin.site.urls),

    path('index/', viewsInformType.index),
    path('ajaxSaveInformType/', viewsInformType.ajaxSaveInformType),
    path('ajaxDelInformType/', viewsInformType.ajaxDelInformType),
    path('gridDataInformType/', viewsInformType.gridDataInformType),

    path('indexTarget/', viewsInformType.indexTarget),
    path('setInformTarget/', viewsInformType.setInformTarget),
]
