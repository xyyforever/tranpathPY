from django.urls import path
from system.views import viewsPurview

urlpatterns = [
    # path('admin/', admin.site.urls),

    path('index/', viewsPurview.index),
    path('ajaxSavePurview/', viewsPurview.ajaxSavePurview),
    path('ajaxDelPurview/', viewsPurview.ajaxDelPurview),
    path('gridDataPurview/', viewsPurview.gridDataPurview),
    path('moveSortsPurview/', viewsPurview.ajaxMoveSortsPurview),

]
