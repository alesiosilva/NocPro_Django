from django.shortcuts import render
import requests
from django.contrib.auth.decorators import login_required
import base64

servidor = "url"
api_user = "user"
api_senha = "senha"
data_string = api_user + ":" + api_senha
authorization = data_string.encode("utf-8")
authorization = base64.b64encode(authorization)
authorization = authorization.decode("utf-8")
authorization = "Basic " + str(authorization)


@login_required
def ativos_list(request):
    response = requests.get(servidor + '/tas/api/assetmgmt/assets?fields=unid,specification,name&templateName=Backbone',
    #headers={'content-type': 'application/json', 'Authorization': 'Basic Y2FybG9zLnNvdXNhOjN6dmc1LWl1MnJyLW5qcW82LW15dGlnLXdibmFs'})
    headers={'content-type': 'application/json', 'Authorization': authorization})
    ativos = response.json()
    return render(request, 'topdesk/ativos_list.html', {
        'ativos_list': ativos['dataSet']
    })
