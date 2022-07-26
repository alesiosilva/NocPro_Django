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
    #atual_status = request.POST.getlist('atual_status')
    inputs_nova_fila = request.POST.get('nova_fila')
    inputs_nota = request.POST.get('nota') + '<br/><br/>Alteração massiva: ' + str(request.user.first_name)
    inputs_alterar = request.POST.getlist('alterar')

    #return HttpResponse(inputs_alterar)
    #response = json.dumps(
    #    {
    #        'inputs_status': inputs_status,
    #        'inputs_alterar': inputs_alterar
    #    }
    #)
    #return HttpResponse(response, content_type='application/json')

    #chamados = json.dumps(inputs_alterar)

    #for chamado in inputs_alterar:
    #    chamados_atualizados = rest_post_update(chamado,inputs_status,inputs_nota)
    #    chamados = chamados + ',' + chamados_atualizados['number']

    data = []
    #i = 0
    for chamado in inputs_alterar:

        new_status = inputs_status

        chamados_atualizados = rest_post_update(chamado, new_status, inputs_nova_fila, inputs_nota)
        item = {
            "number": chamados_atualizados['number'],
            "briefDescription": chamados_atualizados['briefDescription'],
            "processingStatus": chamados_atualizados['processingStatus']
            #"processingStatus": new_status
        }
        data.append(item)
        #i = i + 1

    #chamados = json.dumps(data)
    chamados = data
    #    x = chamado
    #return HttpResponse(x)

    #return HttpResponse("chamados atualizados")
    #return HttpResponse(inputs_status)

    #return HttpResponse(chamados, content_type='application/json')
    return render(request, 'topdesk/ticket_update.html', {'tickets_list': chamados})


def rest_post_update(chamado,inputs_status,inputs_nova_fila,inputs_nota):
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

            # validar se status será alterado
            if inputs_status == "-":
                ticket_create_json = {
                    #'processingStatus':
                    #    {'name': inputs_status},
                    'operatorGroup':
                        {'id': inputs_nova_fila},
                    'action': inputs_nota
                }
            elif inputs_nova_fila == "-":
                ticket_create_json = {
                    'processingStatus':
                        {'name': inputs_status},
                    #'operatorGroup':
                    #    {'id': inputs_nova_fila},
                    'action': inputs_nota
                }
            else:
                ticket_create_json = {
                    'processingStatus':
                        {'name': inputs_status},
                    'operatorGroup':
                        {'id': inputs_nova_fila},
                    'action': inputs_nota
                }

            response = requests.put(model_servers.host + url_complement,
            headers={'content-type': 'application/json', 'Authorization': authorization},
            data=json.dumps(ticket_create_json)
            )
            tickets = response.json()

            #return render(request, 'topdesk/massive_change.html', {'tickets_list': tickets})
            #return HttpResponse(tickets, content_type='application/json')
            return tickets
        else:
            return HttpResponseRedirect("/servers_create")

    except requests.exceptions.ConnectionError as e:
        return HttpResponse("Erro ao conectar no servidor")


@login_required
def massive_change(request):
    data = {}
    data['usuario'] = request.user

    #recurar grupos de operadores
    groups = list_operatorgroups()
    return render(request, 'topdesk/massive_change.html', {'groups': groups, 'user': data})


def list_operatorgroups():
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

            url_complement = '/tas/api/operatorgroups?page_size=100&'
            url_complement = url_complement + 'query=groupName=sw=(\'GTI\')' + ','
            url_complement = url_complement + 'groupName=sw=(\'CAIS\')'
            #url_complement = url_complement + 'fields=id,number,briefDescription,processingStatus.name'

            response = requests.get(model_servers.host + url_complement,
            #headers={'content-type': 'application/json', 'Authorization': 'Basic xxxxxxxxxxx'})
            headers={'content-type': 'application/json', 'Authorization': authorization})
            tickets = response.json()


            #return render(request, 'topdesk/massive_change.html', {'tickets_list': tickets})
            #return HttpResponse(response, content_type='application/json')
            return tickets
        else:
            return HttpResponseRedirect("/servers_create")

    except requests.exceptions.ConnectionError as e:
        return HttpResponse("Erro ao conectar no servidor")


@login_required
def lista_chamados(self):
    try:
        if Servers.objects.filter(nome="topdesk"):

            filtro_fila = self.POST.get('fila')
            #filtro_fila = filtro_fila.replace(" ", "%20")

            model_servers = Servers.objects.get(nome="topdesk")
            # servidor = model_servers.host
            api_user = model_servers.user
            api_senha = model_servers.password
            data_string = api_user + ":" + api_senha
            authorization = data_string.encode("utf-8")
            authorization = base64.b64encode(authorization)
            authorization = authorization.decode("utf-8")
            authorization = "Basic " + str(authorization)

            url_complement = '/tas/api/incidents?page_size=50&'
            url_complement = url_complement + 'query=operatorGroup.name==' + filtro_fila + ';'
            url_complement = url_complement + 'processingStatus.name!=Fechado&'
            url_complement = url_complement + 'fields=id,number,briefDescription,processingStatus.name,operator.name'

            response = requests.get(model_servers.host + url_complement,
            #headers={'content-type': 'application/json', 'Authorization': 'Basic xxxxxxxxxxx'})
            headers={'content-type': 'application/json', 'Authorization': authorization})
            #tickets = response.json()


            #return render(request, 'topdesk/massive_change.html', {'tickets_list': tickets})
            return HttpResponse(response, content_type='application/json')
        else:
            return HttpResponseRedirect("/servers_create")

    except requests.exceptions.ConnectionError as e:
        return HttpResponse("Erro ao conectar no servidor")


@login_required
def ativos_list(request):
    data = {}
    data['usuario'] = request.user
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
            return render(request, 'topdesk/ativos_list.html', {'ativos_list': ativos['dataSet'], 'user': data})
        else:
            return HttpResponseRedirect("/servers_create")

    except requests.exceptions.ConnectionError as e:
        return HttpResponse("Erro ao conectar no servidor")
