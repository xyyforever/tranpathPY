from django.urls import path
from system.views import viewsSeller

# 添加到urls.py
# path('seller/',include("system.urlsSeller")),

urlpatterns = [
    # path('admin/', admin.site.urls),

    path('index/', viewsSeller.index),
    path('ajaxSaveSeller/', viewsSeller.ajaxSaveSeller),
    path('ajaxDelSeller/', viewsSeller.ajaxDelSeller),
    path('gridDataSeller/', viewsSeller.gridDataSeller),

]
