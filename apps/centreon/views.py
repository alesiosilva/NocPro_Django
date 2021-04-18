from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import ListView
from django.shortcuts import render
import requests
#from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from apps.core.models import Servers

#if Servers.objects.filter(nome="centreon"):
#    model_servers = Servers.objects.get(nome="centreon")
#    centreon_servidor = model_servers.host
#    centreon_api_user = model_servers.user
#    centreon_api_senha = model_servers.password

def autenticar():
    try:
        model_servers = Servers.objects.get(nome="centreon")
        response = requests.post(model_servers.host + '/centreon/api/index.php?action=authenticate',
        data={'username': model_servers.user, 'password': model_servers.password})
        token = response.json()
        return token['authToken']
    except requests.exceptions.ConnectionError:
        return "123456"

@login_required
def host_list(request):
        try:
            model_servers = Servers.objects.get(nome="centreon")
            if Servers.objects.filter(nome="centreon"):
                response = requests.get(model_servers.host + '/centreon/api/index.php?object=centreon_realtime_hosts&sortType=id&order=desc&action=list&fields=id,name,notes,address',
                headers={'content-type': 'application/json', 'centreon-auth-token': autenticar()})
                hosts = response.json()
                return render(request, 'centreon/host_list.html', {
                    'host_list': hosts
                })
            else:
                return HttpResponseRedirect("/servers_create")

        except requests.exceptions.ConnectionError as e:
            return HttpResponse("Erro ao conectar no servidor")


def host_field():
        try:
            model_servers = Servers.objects.get(nome="centreon")
            if Servers.objects.filter(nome="centreon"):
                response = requests.get(model_servers.host + '/centreon/api/index.php?object=centreon_realtime_hosts&sortType=id&order=desc&action=list&fields=id,name,notes,address',
                headers={'content-type': 'application/json', 'centreon-auth-token': autenticar()})
                hosts = response.json()
                #return hosts[1]['id']
                return hosts
            else:
                # return HttpResponseRedirect("servers_create")
                hosts = ()
                return hosts
        except requests.exceptions.ConnectionError:
            hosts = ()
            return hosts


