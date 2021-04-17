from django.contrib import admin
from django.urls import path
from .views import home, ServersList, serversCreate, ServersDelete
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', home, name='home'),
    path('servers/', login_required(ServersList.as_view()), name='servers'),
    path('servers_create/', login_required(serversCreate), name='servers_create'),
    path('servers_delete/<int:pk>', login_required(ServersDelete.as_view()), name='servers_delete'),
    ]
