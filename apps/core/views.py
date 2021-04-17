from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Servers
from django.views.generic import ListView, CreateView, DeleteView
from django import forms
from django.urls import reverse, reverse_lazy

@login_required
def home(request):
    data = {}
    data['usuario'] = request.user
    return render(request, 'core/index.html', data)


class ServersList(ListView):
    model = Servers


class ServersForm(forms.ModelForm):
    class Meta:
        model = Servers
        fields = "__all__"
        widgets = {
            'password': forms.PasswordInput()
        }


def serversCreate(request):
    if request.method == "POST":
        form = ServersForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/servers')
            except:
                pass
    else:
        form = ServersForm()
    return render(request, 'core/servers_form.html/', {'form': form})


class ServersDelete(DeleteView):
    model = Servers
    success_url = reverse_lazy('servers')