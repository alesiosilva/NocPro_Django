from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from apps.centreon.views import host_field
import requests


class Acionamento(models.Model):

    #nome = models.CharField(max_length=100)
    nome = models.ForeignKey(User, on_delete=models.PROTECT)
    email = models.EmailField(blank=True, default="")
    telefone = models.CharField(max_length=50)

    hosts_arg = host_field()
    
    hosts =  ()
    for hosts_array in hosts_arg:

        hosts += (
            (hosts_array['name'], hosts_array['name']),
        )

    ativos = models.CharField(max_length=100, choices=hosts)
    #ativos = models.CharField(teste, max_length=100)

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('list_acionamentos')