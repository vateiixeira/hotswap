from my_project.core.tasks import envia_email_chamado
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render,redirect, get_object_or_404
from my_project.chamado.models import Chamado
from my_project.chamado.forms import ChamadoForm
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from my_project.core.utils import render_to_pdf, Render
from datetime import datetime, timedelta
from django.utils import timezone
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
        model.equipamento = Equipamento.object.filter(serial=model.serial).last()
        model.loja = Lojas.object.get(id=request.POST.get('loja'))
        model.defeito = request.POST.get('defeito')
        
        valor = request.POST.get('valor')
        valor = valor.replace(',','.')
        model.valor = valor
        
        model.status = request.POST.get('status')
        model.fornecedor = Fornecedor.object.get(id=request.POST.get('fornecedor'))
        model.justificativa = request.POST.get('justificativa')
        model.nfe = request.POST.get('nfe')
        model.user = usuario    
        try:
            model.save()
            model.refresh_from_db()
            envia_email_chamado.delay(model.id)
            return redirect('core:homepage')
        except Exception as ex:
            return HttpResponseBadRequest(ex)
    else:
        form = ChamadoForm()
    context = {
        "form": form
    }
    return render(request,template,context)

def garantia_equipamento(request):
    if request.method =='POST':
        serial = request.POST.get('serial')
        chamado = Chamado.object.filter(serial=serial, dt_finalizado__isnull=False).order_by('-dt_finalizado')
        if chamado:
            ultimo_chamado = chamado.first()
            if not ultimo_chamado.fornecedor:
                return HttpResponse('Equipamento com chamado, mas sem fornecedor cadastrado.')
            if ultimo_chamado.dt_finalizado + timedelta(days=ultimo_chamado.fornecedor.garantia) > timezone.now().date():
                dias_garantia = (ultimo_chamado.dt_finalizado + timedelta(days=ultimo_chamado.fornecedor.garantia)) - timezone.now().date()
                return HttpResponse('Equipamento ainda possui {} dias de garantia.'.format(dias_garantia.days))
            else:
                dias_apos_garantia = timezone.now().date() - (ultimo_chamado.dt_finalizado + timedelta(days=ultimo_chamado.fornecedor.garantia))
                return HttpResponse('Perdeu garantia há {} dias'.format(dias_apos_garantia.days))
        else:
            return HttpResponse('Equipamento sem abertura de chamado até entao.')


def lista_chamado(request):
    template='lista_chamado.html'


    # grupo_usuario = Profile.objects.get(user = request.user)
    # if grupo_usuario.grupo == "BH":
    #     chamado = Chamado.object.filter(Q(loja_id__in = lista_id_bh)).order_by('-create_at')
    # elif grupo_usuario.grupo == "MONTES CLAROS":
    #     chamado = Chamado.object.filter(Q(loja_id__in = lista_id_moc)).order_by('-create_at')
    # else:
    #     chamado = Chamado.object.all().order_by('-create_at')

    chamado = Chamado.object.filter(loja__in=request.user.profile.filiais.all()).order_by('-create_at')

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

    chamado = Chamado.object.filter(loja__in=request.user.profile.filiais.all(),status = Chamado.STATUS_CHAMADO_PENDENTE)

    # if grupo_usuario.grupo == "BH":
    #     chamado = Chamado.object.filter(Q(loja_id__in = lista_id_bh), status = 'p')
    # elif grupo_usuario.grupo == "MONTES CLAROS":
    #     chamado = Chamado.object.filter(Q(loja_id__in = lista_id_moc), status = 'p')
    # else:
    #     chamado = Chamado.object.filter(status = 'p')

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
        chamado = Chamado.object.filter(create_at__lte=dtfinal, create_at__gte=dtinicial).select_related('equipamento')
        
        # PEGA O SERIAL DOS CHAMADOS EM QUESTAO E JOGA NUMA LISTA
        # DEPOIS FAZ UMA QUERYSET PARA PEGAR OS DADOS DO PRODUTO
        # list_produtos = []
        # for i in chamado:
        #     list_produtos.append(i.serial)
        #equipamento = Equipamento.object.filter(serial__in = list_produtos)
        from django.db.models import Sum

        totais = []
        totais_valor = []
        total_valor_geral = 0
        status_capturados = list(chamado.order_by('status').distinct('status').values_list('status',flat=True))
        for i in status_capturados:
            totais.append(f'{chamado.filter(status=i).last().chamado_verbose()}: {chamado.filter(status=i).count()}')
            valor = chamado.filter(status=i).aggregate(Sum("valor"))["valor__sum"]
            totais_valor.append(f'Valor {chamado.filter(status=i).last().chamado_verbose()}: {valor}')
            total_valor_geral += valor
     
        if not chamado.exists():
            return redirect('core:erro_relatorio')  
        params = {
            #'equipamento':equipamento,
            'chamado': chamado,
            'dtgeracao': dtgeracao,
            'dtinicial': dtinicial,
            'dtfinal': dtfinal,
            'titulo': titulo,
            'totais': totais,
            'totais_valor': totais_valor,
            'total_valor_geral': total_valor_geral,
            'total_geral': chamado.count()
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

        from django.db.models import Sum

        totais = []
        totais_valor = []
        total_valor_geral = 0
        status_capturados = list(chamado.order_by('status').distinct('status').values_list('status',flat=True))
        for i in status_capturados:
            totais.append(f'{chamado.filter(status=i).last().chamado_verbose()}: {chamado.filter(status=i).count()}')
            valor = chamado.filter(status=i).aggregate(Sum("valor"))["valor__sum"]
            totais_valor.append(f'Valor {chamado.filter(status=i).last().chamado_verbose()}: {valor}')
            total_valor_geral += valor
     
        params = {
            'chamado': chamado,
            'dtgeracao': dtgeracao,
            'dtinicial': dtinicial,
            'dtfinal': dtfinal,
            'loja': loja,
            'origem': origem,
            'titulo': titulo,
            'totais': totais,
            'totais_valor': totais_valor,
            'total_valor_geral': total_valor_geral,
            'total_geral': chamado.count()
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

        from django.db.models import Sum

        totais = []
        totais_valor = []
        total_valor_geral = 0
        status_capturados = list(chamado.order_by('status').distinct('status').values_list('status',flat=True))
        for i in status_capturados:
            totais.append(f'{chamado.filter(status=i).last().chamado_verbose()}: {chamado.filter(status=i).count()}')
            valor = chamado.filter(status=i).aggregate(Sum("valor"))["valor__sum"]
            totais_valor.append(f'Valor {chamado.filter(status=i).last().chamado_verbose()}: {valor}')
            total_valor_geral += valor


        if not chamado:
            return redirect('core:erro_relatorio')
        params = {
            'usuario': usuario,
            'chamado': chamado,
            'dtgeracao': dtgeracao,
            'dtinicial': dtinicial,
            'dtfinal': dtfinal,
            'titulo': titulo,
            'totais': totais,
            'totais_valor': totais_valor,
            'total_valor_geral': total_valor_geral,
            'total_geral': chamado.count()
        }

        return Render.render('pdf_usuario.html', params)    

#FIM ENVIO POR USUARIO



