from django.urls import path
from .views import host_list

urlpatterns = [
    #path('', HostList.as_view(), name='list_hosts'),
    path('', host_list, name='host_list'),
    ]
