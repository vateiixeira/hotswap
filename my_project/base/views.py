from django.shortcuts import render,redirect
from . import import_circuito_dados,import_inauguracao, import_circuito_voz,import_lojas
import os
from .models import CentralTelefonica, CircuitoVoz, CircuitoDados,IpFixo, Ferias
from django.views.generic.edit import UpdateView,DeleteView
from my_project.core.utils import is_staff
from django.urls import reverse_lazy
from .forms import *
from django.contrib import messages
from my_project.core.utils import is_staff
from my_project.atendimento.models import Atendimento
from my_project.chamado.models import Chamado


class UpdateCentralTelefonica(UpdateView):
    model = CentralTelefonica
    # fields = '__all__'
    template_name = 'update_central_telefonica.html'
    form_class = CentralTelefonicaForm

class DeleteCentralTelefonica(DeleteView):
    template_name = 'delete_central_telefonica.html'
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
    user = request.user
    staff = is_staff(user)
    context = {
        'staff': staff,
        'chamado': query,
    }
    return render(request,template,context)

class Update_Circuito_Voz(UpdateView):
    model = CircuitoVoz
    # fields = ('__all__')
    template_name = 'update_circuito_voz.html'   
    success_url = reverse_lazy('base:list_circuito_voz')
    form_class = Circuito_VozForm

    def get_object(self, queryset=None):
        model = CircuitoVoz.objects.get(pk=self.kwargs['pk'])
        return model

    context_object_name = 'model'


class Delete_Circuito_Voz(DeleteView):
    template_name = 'delete_ferias.html'
    model = CircuitoVoz
    success_url = reverse_lazy('base:list_circuito_voz')


def list_circuito_dados(request):
    template = 'list_circuito_dados.html'
    query = CircuitoDados.objects.all()

    user = request.user
    staff = is_staff(user)  
    context = {
        'staff': staff,
        'chamado': query
    }
    return render(request,template,context)


class Update_Circuito_Dados(UpdateView):
    model = CircuitoDados
    fields = ('__all__')
    template_name = 'update_circuito_dados.html'   
    success_url = reverse_lazy('base:list_circuito_dados')

    def get_object(self, queryset=None):
        model = CircuitoDados.objects.get(pk=self.kwargs['pk'])
        return model

    context_object_name = 'model'


class Delete_Circuito_Dados(DeleteView):
    template_name = 'delete_ferias.html'
    model = CircuitoDados
    success_url = reverse_lazy('base:list_circuito_dados')


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


def ferias(request):
    template = 'ferias.html'
    query = Ferias.objects.all()

    user = request.user
    staff = is_staff(user)    
    context = {
        'staff': staff,
        "chamado": query
    }

    return render(request,template,context)


class UpdateFerias(UpdateView):
    model = Ferias
    fields = ('__all__')
    template_name = 'update_ferias.html'   
    success_url = reverse_lazy('base:ferias') 

    def get_object(self, queryset=None):
        model = Ferias.objects.get(pk=self.kwargs['pk'])
        return model

    context_object_name = 'model'


class DeleteFerias(DeleteView):
    template_name = 'delete_ferias.html'
    model = Ferias
    success_url = reverse_lazy('base:ferias')



def camara_fria(request):
    template = 'camara_fria.html'
    query = IpFixo.objects.all()

    user = request.user
    staff = is_staff(user)
    context = {
        'staff': staff,
        "chamado": query
    }


    return render(request,template,context)


class UpdateCamara_Fria(UpdateView):
    model = IpFixo
    fields = ('__all__')
    template_name = 'update_camara_fria.html'   
    success_url = reverse_lazy('base:camara_fria') 

    def get_object(self, queryset=None):
        model = IpFixo.objects.get(pk=self.kwargs['pk'])
        return model

    context_object_name = 'model'


class DeleteCamara_Fria(DeleteView):
    template_name = 'delete_ferias.html'
    model = IpFixo
    success_url = reverse_lazy('base:ferias')


def lista_atendimento(request):
    template= 'lista_atendimento_base.html'

    envio = Atendimento.object.filter(status='r').order_by('-create_at')

    context = {
        "envio" : envio
    }
    return render(request,template,context)

def lista_chamado(request):
    template='lista_chamado_base.html'

    chamado = Chamado.object.all().order_by('-create_at')

    context = {
        'chamado': chamado,
    }
    return render(request,template,context)