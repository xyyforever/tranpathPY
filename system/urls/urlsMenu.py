from django.urls import path
from system.views import viewsMenu

urlpatterns = [
    #path('admin/', admin.site.urls),

    path('index/', viewsMenu.index),
    path('getTreeJson/', viewsMenu.ajaxMenuTreeJson),
    path('getMainMenuJson/', viewsMenu.ajaxMainMenuJson),#获取主菜单数据
    path('ajaxSaveMenu/', viewsMenu.ajaxSaveMenu),
    path('moveSorts/', viewsMenu.ajaxMoveSorts),
    path('delMenu/', viewsMenu.ajaxDelMenu)
]