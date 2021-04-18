from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import ListView
from django.shortcuts import render
import requests
#from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from apps.core.models import Servers

if Servers.objects.filter(nome="centreon"):
    model_servers = Servers.objects.get(nome="centreon")
    centreon_servidor = model_servers.host
    centreon_api_user = model_servers.user
    centreon_api_senha = model_servers.password

def autenticar():
    try:
        response = requests.post(centreon_servidor + '/centreon/api/index.php?action=authenticate',
        data={'username': centreon_api_user, 'password': centreon_api_senha})
        token = response.json()
        return token['authToken']
    except requests.exceptions.ConnectionError:
        return "123456"

@login_required
def host_list(request):
    if Servers.objects.filter(nome="centreon"):
        try:
            response = requests.get(centreon_servidor + '/centreon/api/index.php?object=centreon_realtime_hosts&sortType=id&order=desc&action=list&fields=id,name,notes,address',
            headers={'content-type': 'application/json', 'centreon-auth-token': autenticar()})
            hosts = response.json()
            return render(request, 'centreon/host_list.html', {
                'host_list': hosts
            })
        except requests.exceptions.ConnectionError as e:
            return HttpResponse("Erro ao conectar no servidor")
    else:
        return HttpResponseRedirect("/servers_create")


def host_field():
    if Servers.objects.filter(nome="centreon"):
        try:
            response = requests.get(centreon_servidor + '/centreon/api/index.php?object=centreon_realtime_hosts&sortType=id&order=desc&action=list&fields=id,name,notes,address',
            headers={'content-type': 'application/json', 'centreon-auth-token': autenticar()})
            hosts = response.json()
            #return hosts[1]['id']
            return hosts
        except requests.exceptions.ConnectionError:
            hosts = ()
            return hosts
    else:
        #return HttpResponseRedirect("servers_create")
        hosts = ()
        return hosts


