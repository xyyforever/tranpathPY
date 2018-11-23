from django.urls import path
from system.views import viewsUser

# 添加到urls.py
# path('user/',include("system.urlsUser")),

urlpatterns = [
    # path('admin/', admin.site.urls),

    path('index/', viewsUser.index),
    path('ajaxSaveUser/', viewsUser.ajaxSaveUser),
    path('ajaxDelUser/', viewsUser.ajaxDelUser),
    path('gridDataUser/', viewsUser.gridDataUser),
    path('setMenu/', viewsUser.setUserMenu),
    path('setPur/', viewsUser.setUserPur),
    path('setRole/', viewsUser.setUserRole),
    path('setSeller/', viewsUser.setUserSeller),
    path('setPara/', viewsUser.setUserPara),
    path('set_dic/', viewsUser.setUserDic),

]

