from django.urls import path
from .views import ativos_list

urlpatterns = [
    #path('', HostList.as_view(), name='list_hosts'),
    path('', ativos_list, name='ativos_list'),
    ]
