from django.shortcuts import render,redirect, get_object_or_404
from my_project.chamado.models import Chamado
from my_project.chamado.forms import ChamadoForm
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from my_project.core.utils import render_to_pdf, Render
from datetime import datetime
from django.views.generic import View
from .forms import *
from my_project.core.utils import is_staff
from django.contrib.auth.models import User
from django import forms
from django.db.models import Q
from my_project.core.models import Profile,Lojas
from my_project.estoque.models import Equipamento
from my_project.atendimento.views import lista_id_bh, lista_id_moc


# @login_required
# def cadastro(request):
#     template= 'add_chamado.html'  
#     model = Chamado()
#     usuario = request.user

#     if request.method =='POST':
#         context = {}
#         form = ChamadoForm(request.POST)
#         if form.is_valid():
#             model.chamado = form.cleaned_data['chamado']
#             model.modelo = form.cleaned_data['modelo']
#             model.serial = form.cleaned_data['serial']
#             model.loja = form.cleaned_data['loja']
#             model.defeito = form.cleaned_data['defeito'] 
#             model.valor = form.cleaned_data['valor']
#             model.status = form.cleaned_data['status']
#             model.user = usuario    
#             model.save()
#             form = ChamadoForm()
#             messages.success(request, 'Chamado cadastrado com sucesso!')
#             context = {'messages': messages}
#         else:
#             messages.error(request, 'Formulário inválido!')
#             context = {'messages': messages}
#     else:
#         form = ChamadoForm()
#     context = {
#         "form": form
#     }
#     return render(request,template,context)

@login_required
def cadastro(request):
    template= 'add_chamado.html'  
    model = Chamado()
    usuario = request.user

    if request.method =='POST':
        context = {}
        form = ChamadoForm(request.POST)
        model.chamado = request.POST.get('chamado')
        model.modelo = request.POST.get('modelo')
        model.serial = request.POST.get('serial')        
        model.loja = Lojas.object.get(id=request.POST.get('loja'))
        model.defeito = request.POST.get('defeito')
        model.valor = request.POST.get('valor')
        model.status = request.POST.get('status')
        model.user = usuario    
        model.save()
    else:
        form = ChamadoForm()
    context = {
        "form": form
    }
    return render(request,template,context)


def lista_chamado(request):
    template='lista_chamado.html'


    grupo_usuario = Profile.objects.get(user = request.user)
    if grupo_usuario.grupo == "BH":
        chamado = Chamado.object.filter(Q(loja_id__in = lista_id_bh)).order_by('-create_at')
    elif grupo_usuario.grupo == "MONTES CLAROS":
        chamado = Chamado.object.filter(Q(loja_id__in = lista_id_moc)).order_by('-create_at')
    else:
        chamado = Chamado.object.all().order_by('-create_at')

    user = request.user
    staff = is_staff(user)
    context = {
        'chamado': chamado,
        'staff': staff,
    }
    return render(request,template,context)


def lista_chamado_pendente(request):
    template='lista_chamado_pendente.html'
    grupo_usuario = Profile.objects.get(user = request.user)

    if grupo_usuario.grupo == "BH":
        chamado = Chamado.object.filter(Q(loja_id__in = lista_id_bh), status = 'p')
    elif grupo_usuario.grupo == "MONTES CLAROS":
        chamado = Chamado.object.filter(Q(loja_id__in = lista_id_moc), status = 'p')
    else:
        chamado = Chamado.object.filter(status = 'p')

    user = request.user
    staff = is_staff(user)
    context = {
        'chamado': chamado,
        'staff': staff,
    }
    return render(request,template,context)

class DeleteChamado(DeleteView):
    template_name='delete_chamado.html'
    model = Chamado
    success_url = reverse_lazy('chamado:lista_chamado')


def update_chamado(request,pk):
    template = 'update_chamado.html'
    model = Chamado.object.get(pk=pk)

    if request.method == 'POST':
        form = UpdateChamadoForm(request.POST, instance=model)
        if form.is_valid():
            form.save()
            return redirect('chamado:lista_chamado')
    else:
        form = UpdateChamadoForm(instance=model)
    
    context = {
        'form':form,
        'model':model
    }
    return render(request,template,context)

# INICIO SESSÃO DE VIEWS PARA PDF

def chamado_por_data(request):
    template = 'viewpordata.html'
    dtinicial = dtfinal = 0
    if request.method == 'POST':
        form = RelatorioDataForm(request.POST)
        if form.is_valid():
            dtinicial = str(form.cleaned_data['inicial'])
            dtfinal = str(form.cleaned_data['final'])
            return redirect('chamado:pdfdata',dtinicial=dtinicial, dtfinal=dtfinal) 
        else:
            messages.error(request, "Formulário invalido!")            
            form = RelatorioDataForm()
    else: 
        form = RelatorioDataForm()
    context = {
        'form': form
    }    
    return render(request,template, context)

class PdfPorData(View):
    def get(self, request, dtinicial, dtfinal):
        titulo = 'Chamado por data'
        dtgeracao = datetime.now()
        chamado = Chamado.object.filter(create_at__lte=dtfinal, create_at__gte=dtinicial)  
        
        # PEGA O SERIAL DOS CHAMADOS EM QUESTAO E JOGA NUMA LISTA
        # DEPOIS FAZ UMA QUERYSET PARA PEGAR OS DADOS DO PRODUTO
        list_produtos = []
        for i in chamado:
            list_produtos.append(i.serial)
        equipamento = Equipamento.object.filter(serial__in = list_produtos)
     
        if not chamado.exists():
            return redirect('core:erro_relatorio')  
        params = {
            'equipamento':equipamento,
            'chamado': chamado,
            'dtgeracao': dtgeracao,
            'dtinicial': dtinicial,
            'dtfinal': dtfinal,
            'titulo': titulo,
        }
        return Render.render('pdf_chamado.html', params)

#RELATORIO CHAMADO POR FILIAL

def chamado_por_data_filial(request):
    template = 'viewpordatafilial.html'
    dtinicial = dtfinal = 0
    if request.method == 'POST':
        form = RelatorioDataFilialForm(request.POST or None) 
        if form.is_valid():
            dtinicial = str(form.cleaned_data['inicial'])
            dtfinal = str(form.cleaned_data['final'])
            idorigem = request.POST.get('filial')
            return redirect('chamado:pdfdatafilial',dtinicial=dtinicial, dtfinal=dtfinal,idorigem=idorigem) 
        else: 
            messages.error(request, "Formulário invalido!")  
            form = RelatorioDataFilialForm() 
    else: 
        form = RelatorioDataFilialForm()
    context = {
        'form': form
    }    
    return render(request,template, context)

class PdfPorDataFilial(View):
    def get(self, request, dtinicial, dtfinal, idorigem):
        titulo = 'Chamado por data e filial'
        dtgeracao = datetime.now()
        origem = Lojas.object.get(id=idorigem)
        chamado = Chamado.object.filter(create_at__lte=dtfinal, create_at__gte=dtinicial, loja=idorigem) 
        loja = Lojas.object.get(id=idorigem)
        if not chamado.exists():
            return redirect('core:erro_relatorio')
        params = {
            'chamado': chamado,
            'dtgeracao': dtgeracao,
            'dtinicial': dtinicial,
            'dtfinal': dtfinal,
            'loja': loja,
            'origem': origem,
            'titulo': titulo,
        }

        return Render.render('pdf_data_filial.html', params)

# ENVIO POR USUARIO        
def chamado_por_usuario(request):
    template = 'viewporusuario.html'
    dtinicial = dtfinal = 0
    if request.method == 'POST':
        form = RelatorioUsuarioForm(request.POST)
        if form.is_valid():
            dtinicial = str(form.cleaned_data['inicial'])
            dtfinal = str(form.cleaned_data['final'])
            usuario = request.POST.get('usuario')
            return redirect('chamado:pdfusuario',dtinicial=dtinicial, dtfinal=dtfinal, usuario=usuario) 
        else: 
            messages.error(request, "Formulário invalido!")
            form = RelatorioUsuarioForm()
    else: 
        form = RelatorioUsuarioForm()
    context = {
        'form': form
    }    
    return render(request,template, context)

class PdfPorUsuario(View):
    def get(self, request, dtinicial, dtfinal, usuario):
        titulo = 'Chamado por usuário'
        dtgeracao = datetime.now()
        chamado = Chamado.object.filter(create_at__lte=dtfinal, create_at__gte=dtinicial, user_id=usuario)
        usuario = User.objects.get(id=usuario)
        if not chamado:
            return redirect('core:erro_relatorio')
        params = {
            'usuario': usuario,
            'chamado': chamado,
            'dtgeracao': dtgeracao,
            'dtinicial': dtinicial,
            'dtfinal': dtfinal,
            'titulo': titulo,
        }

        return Render.render('pdf_usuario.html', params)    

#FIM ENVIO POR USUARIO

def change_date(request):
    template = 'change_date.html'
    lista_chamados_antigos = [526188,526187,525761,525759,525719,525697,525634,525124,524927,524927,529222,527494,526415,532364,530578,530574,524927,534515,536543,536348,534577,534577,534576,534576,534575,534575,541172,541132,541131,538219,537889,537416,537416,534577,542772,542772,542771,542771,542757,541522,547527,547228,546508,546504,546500,553209,553062,550728,557152,557064,556555,556335,556334,555855,555583,555576,555575,555572,555570,555569,554672,554304,560465,560258,558848,556335,556335,566238,566237,566210,566208,566207,566206,566205,566204,566203,564958,564847,564266,563379,563267,563262,562998,562882,562453,570676,567981,567274,567274,483416,482623,484749,484715,491452,491187,497503,495488,495002,503922,503518,503517,503063,502588,502124,502123,502003,509618,514077,516431,515573,522283,520654,519380,453326,452730,454876,458655,457304,458655,472877,476233,474709,478778,573995,573863,573603,572295,579065,579063,579061,579050,579042,579040,579039,579027,579024,579023,576923,576783,576778,576777,576775,576773,583577,583005,582303,581965,580437,591409,588669,595780,595777,593681,593006,601175,599382,599008,598645,606136,606128,602454,602450,616877,616865,615074,614870,614374,612789,621617,619445]
    obj = Chamado.object.filter(id__in = lista_chamados_antigos)
    for x in obj:
        finalizado = x.dt_finalizado
        x.create_at = finalizado
        x.save()
    return render(request,template)

