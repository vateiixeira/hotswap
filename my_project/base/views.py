from django.shortcuts import render,redirect
from . import import_circuito_dados,import_inauguracao, import_circuito_voz,import_lojas
import os
from .models import CentralTelefonica, CircuitoVoz, CircuitoDados
from django.views.generic.edit import UpdateView,DeleteView
from my_project.core.utils import is_staff
from django.urls import reverse_lazy
from .forms import *
from django.contrib import messages
from my_project.core.utils import is_staff


class UpdateCentralTelefonica(UpdateView):
    model = CentralTelefonica
    fields = ['__all__']
    teamplate = 'update_central_telefonica.html'

class DeleteCentralTelefonica(DeleteView):
    template = 'delete_central_telefonica.html'
    model = CentralTelefonica
    success_url = reverse_lazy('base:list_central_telefonica')

def list_central_telefonica(request):
    template = 'list_central_telefonica.html'
    query = CentralTelefonica.objects.all()
    staff = is_staff(request.user)
    context = {
        'chamado': query,
        'staff': staff,
    }
    return render(request,template,context)

def importar(request):
    template = 'importar.html'
    # IMPORTAR UM DE CADA VEZ PARA NAO FICAR CONFUSO IGUAL UM JEGUE
    #data = import_lojas.csv_to_list(os.path.join(os.path.dirname(os.path.dirname(__file__)),'temp/filial.csv')) 
    #data = import_inauguracao.csv_to_list(os.path.join(os.path.dirname(os.path.dirname(__file__)),'temp/inauguracao.csv'))  
    #data = import_circuito_voz.csv_to_list(os.path.join(os.path.dirname(os.path.dirname(__file__)),'temp/circuito_voz.csv'))  
    #data = import_circuito_dados.csv_to_list(os.path.join(os.path.dirname(os.path.dirname(__file__)),'temp/circuito_dados.csv'))    
    return render(request,template)

def list_circuito_voz(request):
    template = 'list_circuito_voz.html'
    query = CircuitoVoz.objects.all()
    context = {
        'chamado': query,
    }
    return render(request,template,context)

def list_circuito_dados(request):
    template = 'list_circuito_dados.html'
    query = CircuitoDados.objects.all()
    context = {
        'chamado': query
    }
    return render(request,template,context)

def cadastro_incidente(request):

    template = 'cadastro_incidente.html'

    if request.method == 'POST':
        form = IncidenteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Incidente cadastrado com sucesso!')
    else:
       form = IncidenteForm() 

    context = {
        'form': form
    }
    return render(request,template,context)

def lista_incidente(request):
    template='lista_incidente.html'
    query = HistoricoIncidente.objects.all()
    staff = is_staff(request.user)
    context = {
        'chamado': query,
        'staff' : staff
    }

    return render(request,template,context)


class DeleteIncidente(DeleteView):
    template_name='delete_incidente.html'
    model = HistoricoIncidente
    success_url = reverse_lazy('base:lista_incidente')

def update_incidente(request,pk):
    template = 'update_incidente.html'
    model = HistoricoIncidente.objects.get(pk=pk)

    if request.method == 'POST':
        form = IncidenteForm(request.POST, instance=model)
        if form.is_valid():
            form.save()
            return redirect('base:lista_incidente')
    else:
        form = IncidenteForm(instance=model)
    
    context = {
        'form':form,
        'model':model
    }
    return render(request,template,context)


def lista_dt_inauguracao(request):
    template = 'list_dt_inauguracao.html'
    query = DataInauguracao.objects.all()
    context = {
        "chamado": query
    }
    return render(request,template,context)