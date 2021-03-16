from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from .models import Acionamento
import requests

class AcionamentosList(ListView):
    model = Acionamento


class AcionamentoCreate(CreateView):
    model = Acionamento
    fields = ['nome','ativos', 'email','telefone']


class AcionamentoEdit(UpdateView):
    model = Acionamento
    fields = ['nome','ativos', 'email','telefone']


