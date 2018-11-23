from django.urls import path
from basicInfo.views import viewsProbrand

# 添加到urls.py
# path('probrand/',include("basicInfo.urlsProbrand")),

urlpatterns = [
    # path('admin/', admin.site.urls),

    path('index/', viewsProbrand.index),
    path('ajaxSaveProbrand/', viewsProbrand.ajaxSaveProbrand),
    path('ajaxDelProbrand/', viewsProbrand.ajaxDelProbrand),
    path('gridDataProbrand/', viewsProbrand.gridDataProbrand),

]