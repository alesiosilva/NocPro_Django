from django.views.generic import ListView
from django.shortcuts import render
import requests
#from django.views.generic import ListView
from django.contrib.auth.decorators import login_required

def autenticar(request):
    response = requests.post(servidor + '/centreon/api/index.php?action=authenticate',
    data={'username': user, 'password': senha})
    token = response.json()
    return token['authToken']

@login_required
def host_list(request):
    response = requests.get(servidor + '/centreon/api/index.php?object=centreon_realtime_hosts&sortType=id&order=desc&action=list&fields=id,name,notes,address',
    headers={'content-type': 'application/json', 'centreon-auth-token': autenticar(request)})
    hosts = response.json()
    return render(request, 'centreon/host_list.html', {
        'host_list': hosts
    })
