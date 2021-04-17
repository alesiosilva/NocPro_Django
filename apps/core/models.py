from django.db import models
from django import forms


class Servers(models.Model):
    nome = models.CharField(max_length=100)
    host = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    password = models.CharField(max_length=100)




