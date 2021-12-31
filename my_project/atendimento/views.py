from my_project.core.tasks import envia_email_atendimento
from django.shortcuts import render
from .forms import RelatorioTecnicoForm,RelatorioCompletoForm, RelatorioSetorForm,RelatorioCompletoTodasForm,AtendimentoViewForm
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from .models import Atendimento
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from my_project.core.utils import render_to_pdf, Render
from django.views.generic import View
from datetime import datetime
from django.contrib.auth.models import User
from .forms import AtendimentoForm
from django.urls import reverse_lazy
from django.forms.models import modelform_factory
from my_project.core.utils import is_staff
from my_project.core.models import Profile
from django.db.models import Q



lista_id_bh = [8,10,12,13,14,15,16,17,18,19,20,21,22,23,24,26,27,28,29,30,31,32,33,34,35]
lista_id_moc = [2,3,4,6,7,9,11,25]

class DeleteAtendimento(DeleteView):
    template_name='delete_atendimento.html'
    model = Atendimento
    success_url = reverse_lazy('atendimento:lista_atendimento')
    

def update_atendimento(request, pk):
    template = 'update_atendimento.html'
    model = Atendimento.object.get(pk=pk)
    context = {}
    if request.method == "POST":
        form = AtendimentoViewForm(request.POST, instance=model)
        if form.is_valid():   

            model.loja = form.cleaned_data['loja']
            model.solicitante = form.cleaned_data['solicitante']
            model.solucao = form.cleaned_data['solucao']
            model.status = form.cleaned_data['status']

            if model.status == 'r':
                model.user_finaliza = request.user

            model.setor = form.cleaned_data['setor']
            model.problema = form.cleaned_data['problema']
            model.save()
            return redirect('/atendimento/')
    else:
        form = AtendimentoViewForm(instance=model)
    context = {
        'staff': is_staff(request.user),
        'form':form,
        'model':model,
    }
    return render(request,template, context)


def add_atendimento(request,user):    
    model = Atendimento()

    if request.method == "POST":
        form = AtendimentoForm(request.POST or None)
        if form.is_valid():
            model.user = user
            model.loja = form.cleaned_data['loja']
            model.solicitante = form.cleaned_data['solicitante']
            model.solucao = form.cleaned_data['solucao']
            model.status = form.cleaned_data['status']
            model.responsavel = form.cleaned_data['responsavel']

            if model.status == 'r':
                model.user_finaliza = request.user
            
            model.setor = form.cleaned_data['setor']        
            model.problema = form.cleaned_data['problema']
            model.save()
            model.refresh_from_db()
            envia_email_atendimento.delay(model.id)
        else:
            form = AtendimentoForm()
            messages.error(request, "Formulário inválido!")


def lista_atendimento(request):
    teamplate= 'lista_atendimento.html'
    
    # grupo_usuario = Profile.objects.get(user = request.user)
    # if grupo_usuario.grupo == "BH":
    #     envio = Atendimento.object.filter(Q(loja_id__in = lista_id_bh)).order_by('-create_at')[:200]
    # elif grupo_usuario.grupo == "MONTES CLAROS":
    #     envio = Atendimento.object.filter(Q(loja_id__in = lista_id_moc)).order_by('-create_at')[:200]
    # else:
    #     envio = Atendimento.object.all().order_by('-create_at')[:200]

    envio = Atendimento.object.filter(loja__in=request.user.profile.filiais.all()).order_by('-create_at')[:200]
    context = {
        "envio" : envio
    }
    return render(request,teamplate,context)
    

# class ListaAtendimento(ListView):
#     template_name='lista_atendimento.html'
#     model = Atendimento
#     context_object_name = 'envio'
#     ordering = ['-create_at']


def lista_atendimento_pendente(request):
    template = 'lista_atendimento_pendente.html'
    
    
    # grupo_usuario = Profile.objects.get(user = request.user)
    # if grupo_usuario.grupo == "BH":
    #     envio = Atendimento.object.filter(Q(status='p') & Q(loja_id__in = lista_id_bh))
    # elif grupo_usuario.grupo == "MONTES CLAROS":
    #     envio = Atendimento.object.filter(Q(status='p') & Q(loja_id__in = lista_id_moc))
    # else:
    #     envio = Atendimento.object.filter(status='p')

    envio = Atendimento.object.filter(loja__in=request.user.profile.filiais.all(), status='p').order_by('-create_at')[:200]

    context = {
        'envio':envio
    }
    return render(request,template,context)

def lista_atendimento_pendente_user(request):
    template = 'lista_atendimento_pendente.html'
    
    
    # grupo_usuario = Profile.objects.get(user = request.user)
    # if grupo_usuario.grupo == "BH":
    #     envio = Atendimento.object.filter(Q(status='p') & Q(loja_id__in = lista_id_bh))
    # elif grupo_usuario.grupo == "MONTES CLAROS":
    #     envio = Atendimento.object.filter(Q(status='p') & Q(loja_id__in = lista_id_moc))
    # else:
    #     envio = Atendimento.object.filter(status='p')

    envio = Atendimento.object.filter(responsavel=request.user, status='p').order_by('-create_at')[:200]

    context = {
        'envio':envio
    }
    return render(request,template,context)

# ENVIO POR USUARIO        
def atendimento_por_tecnico(request):
    template = 'viewportecnico_atendimento.html'
    dtinicial = dtfinal = 0
    if request.method == 'POST':
        form = RelatorioTecnicoForm(request.POST)
        if form.is_valid():
            dtinicial = str(form.cleaned_data['inicial'])
            dtfinal = str(form.cleaned_data['final'])
            usuario = request.POST.get('usuario')
            return redirect('atendimento:pdftecnico',dtinicial=dtinicial, dtfinal=dtfinal, usuario=usuario) 
        else: 
            messages.error(request, "Formulário invalido!")
            form = RelatorioTecnicoForm()
    else: 
        form = RelatorioTecnicoForm()
    context = {
        'staff': is_staff(request.user),
        'form': form
    }    
    return render(request,template, context)

class PdfTecnicoAtendimento(View):
    def get(self, request, dtinicial, dtfinal, usuario):
        titulo = 'Atendimento por técnico'
        dtgeracao = datetime.now()

        abertos = Atendimento.object.filter(create_at__lte=dtfinal, create_at__gte=dtinicial, user_id=usuario)

        finalizados = Atendimento.object.filter(updated_at__lte=dtfinal, updated_at__gte=dtinicial, status = 'r', user_finaliza_id=usuario)

        atendimento = abertos | finalizados

        if not atendimento:
            return redirect('core:erro_relatorio')

        usuario = User.objects.get(id=usuario)
        params = {
            'usuario': usuario,
            'atendimento': atendimento,
            'dtgeracao': dtgeracao,
            'dtinicial': dtinicial,
            'dtfinal': dtfinal,
            'titulo': titulo,
        }
        return Render.render('pdf_tecnico.html', params) 

# ENVIO POR USUARIO        
def atendimento_por_responsavel(request):
    template = 'viewportecnico_atendimento.html'
    dtinicial = dtfinal = 0
    if request.method == 'POST':
        form = RelatorioTecnicoForm(request.POST)
        if form.is_valid():
            dtinicial = str(form.cleaned_data['inicial'])
            dtfinal = str(form.cleaned_data['final'])
            usuario = request.POST.get('usuario')
            return redirect('atendimento:pdftecnico',dtinicial=dtinicial, dtfinal=dtfinal, usuario=usuario) 
        else: 
            messages.error(request, "Formulário invalido!")
            form = RelatorioTecnicoForm()
    else: 
        form = RelatorioTecnicoForm()
    context = {
        'staff': is_staff(request.user),
        'form': form
    }    
    return render(request,template, context)

class PdfResponsavelAtendimento(View):
    def get(self, request, dtinicial, dtfinal, usuario):
        titulo = 'Atendimento por técnico'
        dtgeracao = datetime.now()

        abertos = Atendimento.object.filter(create_at__lte=dtfinal, create_at__gte=dtinicial, responsavel_id=usuario)

        #finalizados = Atendimento.object.filter(updated_at__lte=dtfinal, updated_at__gte=dtinicial, status = 'r', responsavel_id=usuario)
        atendimento = abertos # | finalizados

        if not atendimento:
            return redirect('core:erro_relatorio')

        usuario = User.objects.get(id=usuario)
        params = {
            'usuario': usuario,
            'atendimento': atendimento,
            'dtgeracao': dtgeracao,
            'dtinicial': dtinicial,
            'dtfinal': dtfinal,
            'titulo': titulo,
        }
        return Render.render('pdf_tecnico.html', params)    

#FIM ENVIO POR USUARIO

# ENVIO COMPLETO      
def atendimento_completo(request):
    template = 'viewcompleto_atendimento.html'
    dtinicial = dtfinal = 0
    if request.method == 'POST':
        form = RelatorioCompletoForm(request.POST)
        if form.is_valid():
            dtinicial = str(form.cleaned_data['inicial'])
            dtfinal = str(form.cleaned_data['final'])
            idorigem = request.POST.get('filial')            
            return redirect('atendimento:pdfcompletoatendimento',dtinicial=dtinicial, dtfinal=dtfinal, idorigem=idorigem) 
        else: 
            messages.error(request, "Formulário invalido!")
            form = RelatorioCompletoForm()
    else: 
        form = RelatorioCompletoForm()
    context = {
        'staff': is_staff(request.user),
        'form': form
    }    
    return render(request,template, context)


class PdfCompletoAtendimento(View):
    def get(self, request, dtinicial, dtfinal, idorigem):
        titulo = 'Atendimentos'
        dtgeracao = datetime.now()
        
        geral = Atendimento.object.filter(create_at__lte=dtfinal, create_at__gte=dtinicial, loja=idorigem, updated_at__lte=dtfinal, updated_at__gte=dtinicial)

        #pega os finalizados no periodo filtrado
        fechados = Atendimento.object.filter(updated_at__lte=dtfinal, updated_at__gte=dtinicial, status = 'r', loja=idorigem)

        # junta as duas querysets
        atendimento = geral | fechados
        
        if not atendimento:
            return redirect('core:erro_relatorio')
        params = {
            'atendimento': atendimento,
            'dtgeracao': dtgeracao,
            'dtinicial': dtinicial,
            'dtfinal': dtfinal,
            'titulo': titulo,
        }
        return Render.render('pdf_completo_atendimento.html', params)    

#FIM ENVIO COMPLETO  

# POR SETOR E DATA      
def atendimento_setor(request):
    template = 'viewporsetor_atendimento.html'
    dtinicial = dtfinal = 0
    if request.method == 'POST':
        form = RelatorioSetorForm(request.POST)
        if form.is_valid():
            dtinicial = str(form.cleaned_data['inicial'])
            dtfinal = str(form.cleaned_data['final'])
            idorigem = request.POST.get('setor')            
            return redirect('atendimento:pdfsetoratendimento',dtinicial=dtinicial, dtfinal=dtfinal, idorigem=idorigem) 
        else: 
            messages.error(request, "Formulário invalido!")
            form = RelatorioSetorForm()
    else: 
        form = RelatorioSetorForm()
    context = {
        'staff': is_staff(request.user),
        'form': form
    }    
    return render(request,template, context)

class PdfSetorAtendimento(View):
    def get(self, request, dtinicial, dtfinal, idorigem):
        titulo = 'Atendimentos'
        dtgeracao = datetime.now()
        atendimento = Atendimento.object.filter(create_at__lte=dtfinal, create_at__gte=dtinicial, setor=idorigem)
        if not atendimento:
            return redirect('core:erro_relatorio')
        params = {
            'atendimento': atendimento,
            'dtgeracao': dtgeracao,
            'dtinicial': dtinicial,
            'dtfinal': dtfinal,
            'titulo': titulo,
        }
        return Render.render('pdf_setor_atendimento.html', params)    

#FIM POR SETOR E DATA  

# ENVIO COMPLETO  POR LOJAS    
def atendimento_completo_todas(request):
    template = 'viewcompleto_atendimento_todas.html'
    dtinicial = dtfinal = 0
    if request.method == 'POST':
        form = RelatorioCompletoTodasForm(request.POST)
        if form.is_valid():
            dtinicial = str(form.cleaned_data['inicial'])
            dtfinal = str(form.cleaned_data['final'])         
            return redirect('atendimento:pdfcompletoatendimentotodas',dtinicial=dtinicial, dtfinal=dtfinal) 
        else: 
            messages.error(request, "Formulário invalido!")
            form = RelatorioCompletoTodasForm()
    else: 
        form = RelatorioCompletoTodasForm()
    context = {
        'staff': is_staff(request.user),
        'form': form
    }    
    return render(request,template, context)

class PdfCompletoAtendimentoTodas(View):
    def get(self, request, dtinicial, dtfinal):
        usuario = request.user
        titulo = 'Atendimentos'
        dtgeracao = datetime.now()
        #pega todos criados no periodo filtrado
        geral  = Atendimento.object.filter(create_at__lte=dtfinal, create_at__gte=dtinicial, updated_at__lte=dtfinal, updated_at__gte=dtinicial)
        #pega os finalizados no periodo filtrado
        fechados = Atendimento.object.filter(updated_at__lte=dtfinal, updated_at__gte=dtinicial, status = 'r')

        # junta as duas querysets
        atendimento = geral | fechados

        if not atendimento:
            return redirect('core:erro_relatorio')

        params = {
            'atendimento': atendimento,
            'dtgeracao': dtgeracao,
            'dtinicial': dtinicial,
            'dtfinal': dtfinal,
            'titulo': titulo,
            'usuario':usuario,
        }
        return Render.render('pdf_completo_atendimento_todas.html', params)    