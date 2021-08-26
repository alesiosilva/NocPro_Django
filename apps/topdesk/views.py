import json
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import requests
from django.contrib.auth.decorators import login_required
import base64
from apps.core.models import Servers

#if Servers.objects.filter(nome="topdesk"):
#    model_servers = Servers.objects.get(nome="topdesk")
#    servidor = model_servers.host
#    api_user = model_servers.user
#    api_senha = model_servers.password
#    data_string = api_user + ":" + api_senha
#    authorization = data_string.encode("utf-8")
#    authorization = base64.b64encode(authorization)
#    authorization = authorization.decode("utf-8")
#    authorization = "Basic " + str(authorization)


@login_required
def tickets_update(request):
    inputs_status = request.POST.get('status')
    inputs_alterar = request.POST.getlist('alterar')
    #return HttpResponse(inputs_alterar)
    #response = json.dumps(
    #    {
    #        'inputs_status': inputs_status,
    #        'inputs_alterar': inputs_alterar
    #    }
    #)
    #return HttpResponse(response, content_type='application/json')

    chamados = json.dumps(inputs_alterar)

    for chamado in inputs_alterar:
        rest_post_update(chamado,inputs_status)
    #    x = chamado
    #return HttpResponse(x)

    #return HttpResponse("chamados atualizados")
    #return HttpResponse(inputs_status)

    return HttpResponse(chamados, content_type='application/json')


def rest_post_update(chamado,inputs_status):
    try:
        if Servers.objects.filter(nome="topdesk"):
            model_servers = Servers.objects.get(nome="topdesk")
            # servidor = model_servers.host
            api_user = model_servers.user
            api_senha = model_servers.password
            data_string = api_user + ":" + api_senha
            authorization = data_string.encode("utf-8")
            authorization = base64.b64encode(authorization)
            authorization = authorization.decode("utf-8")
            authorization = "Basic " + str(authorization)

            url_complement = '/tas/api/incidents/id/' + chamado

            ticket_create_json = {
                'processingStatus':
                    {'name': inputs_status}
            }

            response = requests.put(model_servers.host + url_complement,
            headers={'content-type': 'application/json', 'Authorization': authorization},
            data=json.dumps(ticket_create_json)
            )
            tickets = response.json()

            #return render(request, 'topdesk/massive_change.html', {'tickets_list': tickets})
            return HttpResponse(tickets, content_type='application/json')
        else:
            return HttpResponseRedirect("/servers_create")

    except requests.exceptions.ConnectionError as e:
        return HttpResponse("Erro ao conectar no servidor")


@login_required
def massive_change(request):
    try:
        if Servers.objects.filter(nome="topdesk"):
            model_servers = Servers.objects.get(nome="topdesk")
            # servidor = model_servers.host
            api_user = model_servers.user
            api_senha = model_servers.password
            data_string = api_user + ":" + api_senha
            authorization = data_string.encode("utf-8")
            authorization = base64.b64encode(authorization)
            authorization = authorization.decode("utf-8")
            authorization = "Basic " + str(authorization)

            url_complement = '/tas/api/incidents?page_size=20&'
            url_complement = url_complement + 'query=operatorGroup.name==GTI::NOC::NOC-ADM;'
            url_complement = url_complement + 'processingStatus.name!=Fechado&'
            url_complement = url_complement + 'fields=id,number,briefDescription,processingStatus.name'

            response = requests.get(model_servers.host + url_complement,
            #headers={'content-type': 'application/json', 'Authorization': 'Basic xxxxxxxxxxx'})
            headers={'content-type': 'application/json', 'Authorization': authorization})
            tickets = response.json()

            return render(request, 'topdesk/massive_change.html', {'tickets_list': tickets})
        else:
            return HttpResponseRedirect("/servers_create")

    except requests.exceptions.ConnectionError as e:
        return HttpResponse("Erro ao conectar no servidor")


@login_required
def ativos_list(request):
    try:
        if Servers.objects.filter(nome="topdesk"):
            model_servers = Servers.objects.get(nome="topdesk")
            # servidor = model_servers.host
            api_user = model_servers.user
            api_senha = model_servers.password
            data_string = api_user + ":" + api_senha
            authorization = data_string.encode("utf-8")
            authorization = base64.b64encode(authorization)
            authorization = authorization.decode("utf-8")
            authorization = "Basic " + str(authorization)

            response = requests.get(model_servers.host + '/tas/api/assetmgmt/assets?fields=unid,specification,name&templateName=Backbone',
            #headers={'content-type': 'application/json', 'Authorization': 'Basic xxxxxxxxxxx'})
            headers={'content-type': 'application/json', 'Authorization': authorization})
            ativos = response.json()
            return render(request, 'topdesk/ativos_list.html', {'ativos_list': ativos['dataSet']})
        else:
            return HttpResponseRedirect("/servers_create")

    except requests.exceptions.ConnectionError as e:
        return HttpResponse("Erro ao conectar no servidor")
