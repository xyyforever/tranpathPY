from django.urls import path
from system.views import viewsRole

# 添加到urls.py
# path('role/',include("system.urlsRole")),

urlpatterns = [
    # path('admin/', admin.site.urls),

    path('index/', viewsRole.index),
    path('ajaxSaveRole/', viewsRole.ajaxSaveRole),
    path('ajaxDelRole/', viewsRole.ajaxDelRole),
    path('gridDataRole/', viewsRole.gridDataRole),
    path('setMenu/', viewsRole.setRoleMenu),
    path('setPur/', viewsRole.setRolePur),

    path('moveSortsRole/', viewsRole.ajaxMoveSortsRole),

]
