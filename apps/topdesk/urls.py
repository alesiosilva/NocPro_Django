from django.urls import path
from .views import ativos_list,massive_change, tickets_update,lista_chamados

urlpatterns = [
    #path('', HostList.as_view(), name='list_hosts'),
    path('ativos', ativos_list, name='ativos_list'),
    path('', massive_change, name='massive_change'),
    path('tickets_update', tickets_update, name='tickets_update'),
    path('lista_chamados', lista_chamados, name='lista_chamados'),
    ]
