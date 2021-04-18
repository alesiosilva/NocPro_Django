from django.http import HttpResponseRedirect
from django.shortcuts import render
import requests
from django.contrib.auth.decorators import login_required
import base64
from apps.core.models import Servers

if Servers.objects.filter(nome="topdesk"):
    model_servers = Servers.objects.get(nome="topdesk")
    servidor = model_servers.host
    api_user = model_servers.user
    api_senha = model_servers.password
    data_string = api_user + ":" + api_senha
    authorization = data_string.encode("utf-8")
    authorization = base64.b64encode(authorization)
    authorization = authorization.decode("utf-8")
    authorization = "Basic " + str(authorization)


@login_required
def ativos_list(request):
    if Servers.objects.filter(nome="topdesk"):
        response = requests.get(servidor + '/tas/api/assetmgmt/assets?fields=unid,specification,name&templateName=Backbone',
        #headers={'content-type': 'application/json', 'Authorization': 'Basic xxxxxxxxxxx'})
        headers={'content-type': 'application/json', 'Authorization': authorization})
        ativos = response.json()
        return render(request, 'topdesk/ativos_list.html', {
            'ativos_list': ativos['dataSet']
        })
    else:
        return HttpResponseRedirect("/servers_create")
