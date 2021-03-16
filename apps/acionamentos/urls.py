from django.urls import path
from .views import AcionamentosList, AcionamentoCreate, AcionamentoEdit
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', AcionamentosList.as_view(), name='list_acionamentos'),
    #path('', Acionamentos_list, name='acionamentos_list'),
    path('novo/', login_required(AcionamentoCreate.as_view()), name='create_acionamento'),
    path('edit/<int:pk>/', login_required(AcionamentoEdit.as_view()), name='update_acionamento'),
    ]
