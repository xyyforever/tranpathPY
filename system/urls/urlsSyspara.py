from django.urls import path
from system.views import viewsSyspara

# 添加到urls.py
# path('syspara/',include("system.urlsSyspara")),

urlpatterns = [
    # path('admin/', admin.site.urls),

    path('index/', viewsSyspara.index),
    path('ajaxSaveSyspara/', viewsSyspara.ajaxSaveSyspara),
    path('ajaxDelSyspara/', viewsSyspara.ajaxDelSyspara),
    path('gridDataSyspara/', viewsSyspara.gridDataSyspara),

    path('moveSortsSyspara/', viewsSyspara.ajaxMoveSortsSyspara),

    path('indexForSeller/', viewsSyspara.indexForSeller),
    path('sellerSetValue/', viewsSyspara.sellerSetValue),
    path('grid_data_select/', viewsSyspara.grid_data_select),

]
