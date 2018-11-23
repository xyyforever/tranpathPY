from django.urls import path
from system.views import viewsCode

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('code/', viewsCode.code),
]