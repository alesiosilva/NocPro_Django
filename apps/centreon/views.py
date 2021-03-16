from django.views.generic import ListView
from django.shortcuts import render
import requests
#from django.views.generic import ListView
from django.contrib.auth.decorators import login_required

centreon_servidor = "url"
centreon_api_user = "user"
centreon_api_senha = "senha"

def autenticar():
    response = requests.post(centreon_servidor + '/centreon/api/index.php?action=authenticate',
    data={'username': centreon_api_user, 'password': centreon_api_senha})
    token = response.json()
    return token['authToken']

@login_required
def host_list(request):
    response = requests.get(centreon_servidor + '/centreon/api/index.php?object=centreon_realtime_hosts&sortType=id&order=desc&action=list&fields=id,name,notes,address',
    headers={'content-type': 'application/json', 'centreon-auth-token': autenticar()})
    hosts = response.json()
    return render(request, 'centreon/host_list.html', {
        'host_list': hosts
    })

def host_field():
    response = requests.get(centreon_servidor + '/centreon/api/index.php?object=centreon_realtime_hosts&sortType=id&order=desc&action=list&fields=id,name,notes,address',
    headers={'content-type': 'application/json', 'centreon-auth-token': autenticar()})
    hosts = response.json()
    #return hosts[1]['id']
    return hosts



