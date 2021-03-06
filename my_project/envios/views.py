from django.shortcuts import render,redirect
from my_project.estoque.forms import MovimentoForm
from .forms import *
from my_project.envios.models import EnvioBh
from my_project.estoque.models import Movimento
from django.forms import inlineformset_factory
from my_project.core.utils import render_to_pdf, Render
from django.views.generic import View
from django.http import HttpResponse
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from datetime import datetime
from my_project.core.utils import is_staff
from django.db.models import Q
from my_project.core.models import Profile

def lista_envio(request):
    template = 'lista_envio.html'

    # grupo_usuario = Profile.objects.get(user = request.user)
    # if grupo_usuario.grupo == "BH":
    #     envio = EnvioBh.object.filter(Q(filial_origem_id__gt = 8)).order_by('-create_at')
    # elif grupo_usuario.grupo == "MONTES CLAROS":
    #     envio = EnvioBh.object.filter(Q(filial_origem_id__lt = 9)).order_by('-create_at')
    # else:
    envio = EnvioBh.object.all().order_by('-create_at')
    recebimento = Recebimento.object.all().order_by('-create_at')

    

    instancia = Recebimento()    
    if request.method == 'POST':
        objeto = EnvioBh.object.get(id=request.POST.get('envio'))
        instancia.envio = objeto
        instancia.user = request.user
        instancia.save()
        objeto.recebido = True
        objeto.save()     
        return redirect('envios:lista_envio')    
    context = {
        'envio':envio,
        'recebimento':recebimento,
    }
    return render(request,template,context)

def lista_envio_pendente(request):
    template = 'lista_envio_pendente.html'

    # grupo_usuario = Profile.objects.get(user = request.user)
    # if grupo_usuario.grupo == "BH":
    #     envio = EnvioBh.object.filter(Q(filial_origem_id__gt = 8)).order_by('-create_at')
    # elif grupo_usuario.grupo == "MONTES CLAROS":
    #     envio = EnvioBh.object.filter(Q(filial_origem_id__lt = 9)).order_by('-create_at')
    # else:
    envio = EnvioBh.object.filter(recebido=False,filial_origem__in=request.user.profile.filiais.all()).order_by('pk')
    recebimento = Recebimento.object.all().order_by('-pk')   

    instancia = Recebimento()    
    if request.method == 'POST':
        objeto = EnvioBh.object.get(id=request.POST.get('envio'))
        instancia.envio = objeto
        instancia.user = request.user
        instancia.save()
        objeto.recebido = True
        objeto.save()     
        return redirect('envios:lista_envio_pendente')    

    context = {
        'envio':envio,
        'recebimento':recebimento,
    }
    return render(request,template,context)

def envio(request):
    template = 'add_envio.html'
    
    form = EnvioForm()
    formset = MovimentoForm()
        
    if request.method == 'POST':

       #PEGA OS DADOS DO POST E JOGA NAS LISTAS
        for key, values in request.POST.lists():
            if key == 'filial_origem':
                filial_origem = values
            elif key == 'filial_destino':
                filial_destino = values
            elif key == 'num_nota':
                num_nota = values
            elif key == 'num_ficha_transf':
                num_ficha_transf = values
            elif key == 'equipamento':
                equipamento = []
                equipamento = values
            elif key == 'quantidade':
                quantidade = []
                quantidade = values
            elif key == 'defeito':
                defeito = []
                defeito = values 

        envio = EnvioBh()
        envio.filial_origem = Lojas.object.get(id=filial_origem[0]) 
        envio.filial_destino = Lojas.object.get(id=filial_destino[0]) 
        envio.num_nota = num_nota[0]
        envio.num_ficha_transf = num_ficha_transf[0]
        envio.user = request.user
        envio.save()

        # ATUALIZAR ESTOQUE
        enviobh = EnvioBh.object.last()
        # RECEBE ULTIMO ENVIO
        ultimo_envio = enviobh.id    

        # ADICIONA OS ITENS NOS OBJETOS E SALVA DIRETO NO MOVIMENTO
        lista = []
        i = 0
        while i < len(quantidade):
            obj = Movimento(
                equipamento = Equipamento.object.get(id =equipamento[i]),
                envio = EnvioBh.object.get(id =ultimo_envio),
                quantidade = quantidade[i],
                defeito = defeito[i],
            )
            lista.append(obj)
            i = i + 1
        Movimento.object.bulk_create(lista)
                           
        loja_destino = Lojas.object.get(id=filial_destino[0])
        loja_origem = Lojas.object.get(id=filial_origem[0])

        # RECEBE ULTIMA MOVIMENTACAO
        movimentacao = Movimento.object.filter(envio_id=ultimo_envio)

        for item in movimentacao:
            id_equipamento = item.equipamento_id
            quantidade = item.quantidade                
            estoque = Equipamento.object.get(id=id_equipamento)                
            qtd_atual = estoque.qtd
            if estoque.loja == loja_destino:
                qtd_final = qtd_atual + quantidade
                estoque.qtd = qtd_final
                estoque.save()

            elif estoque.loja == loja_origem:
                qtd_final = qtd_atual - quantidade
                estoque.qtd = qtd_final
                estoque.save()
    else:
        form = EnvioForm()
        formset = MovimentoForm()

    context = {
        'staff': is_staff(request.user),
        'form': form,
        'formset': formset,
    }
    return render(request,template,context)



# def envio(request):
#     template = 'add_envio.html'
#     envio_form = EnvioBh()
#     item_movimento = inlineformset_factory(EnvioBh, Movimento, 
#     form=MovimentoForm, extra=0, 
#     can_delete=False,
#     min_num=1, validate_min=True)

#     if request.method == 'POST':
#         form = EnvioForm(request.POST, instance=envio_form, prefix='main')
#         formset = item_movimento(request.POST, instance=envio_form, prefix='product')

#         data = request.POST.get('dados')
#         print(data)
#         if form.is_valid() and formset.is_valid():            
#             form = form.save(commit=False)
#             form.user = request.user
#             form.save()
#             formset.save()
                        
#             # ATUALIZAR ESTOQUE
#             enviobh = EnvioBh.object.last()
#             # RECEBE ULTIMO ENVIO
#             ultimo_envio = enviobh.id 
#             # RECEBE ULTIMA MOVIMENTACAO
#             movimentacao = Movimento.object.filter(envio_id=ultimo_envio)

#             loja_destino = Lojas.object.get(name=envio_form.filial_destino)
#             loja_origem = Lojas.object.get(name=envio_form.filial_origem)

#             for item in movimentacao:
#                 id_equipamento = item.equipamento_id
#                 quantidade = item.quantidade                
#                 estoque = Equipamento.object.get(id=id_equipamento)                
#                 qtd_atual = estoque.qtd
#                 if estoque.loja == loja_destino:
#                     qtd_final = qtd_atual + quantidade
#                     estoque.qtd = qtd_final
#                     estoque.save()

#                 elif estoque.loja == loja_origem:
#                     qtd_final = qtd_atual - quantidade
#                     estoque.qtd = qtd_final
#                     estoque.save()

#             messages.success(request, 'Envio cadastrado com sucesso!')
#             context = {'messages': messages}

#             #LIMPA INSTANCIA PARA NÃO DAR ERRO NO FORMULARIO
#             envio_form = EnvioBh()
#             form = EnvioForm(instance=envio_form, prefix='main')
#             formset = item_movimento(instance=envio_form, prefix='product')

#         else:
#             messages.error(request, 'Formulário inválido!')
#             context = {'messages': messages}
#     else:
#         form = EnvioForm(instance=envio_form, prefix='main')
#         formset = item_movimento(instance=envio_form, prefix='product')

#     context = {
#         'staff': is_staff(request.user),
#         'form': form,
#         'formset': formset,
#     }
#     return render(request,template,context)


def envio_por_data(request):
    template = 'viewpordata_envio.html'
    dtinicial = dtfinal = 0
    if request.method == 'POST':
        form = RelatorioDataForm(request.POST)
        if form.is_valid():
            dtinicial = str(form.cleaned_data['inicial'])
            dtfinal = str(form.cleaned_data['final'])
            return redirect('envios:pdfdata',dtinicial=dtinicial, dtfinal=dtfinal) 
        else:
            messages.error(request, "Formulário invalido!")            
            form = RelatorioDataForm()
    else: 
        form = RelatorioDataForm()
    context = {
        'staff': is_staff(request.user),
        'form': form
    }    
    return render(request,template, context)

class PdfPorData(View):
    def get(self, request, dtinicial, dtfinal):
        titulo = 'Envios por data'
        dtgeracao = datetime.now()
        lista = []
        # FORMATO DATA = ANO/MES/DIA
        #FILTRA OS ENVIOS PELA DATA DIGITADA
        envios = EnvioBh.object.filter(create_at__lte=dtfinal, create_at__gte=dtinicial)
        #PEGA OS ID DOS ENVIOS E FILTRA PELO MOVIMENTO PARA PEGAR OS EQUIPAMENTOS UTILIZADOS
        for i in envios:
            lista.append(i.id)
        movimento = Movimento.object.filter(envio_id__in=lista)

        params = {
            'titulo': titulo,
            'envios': envios,
            'movimento': movimento,
            'dtgeracao': dtgeracao,
            'dtinicial': dtinicial,
            'dtfinal': dtfinal,
        }

        return Render.render('pdf_data_envio.html', params)

def envio_por_data_filial(request):
    template = 'viewpordatafilial.html'
    dtinicial = dtfinal = 0
    if request.method == 'POST':
        form = RelatorioDataFilialForm(request.POST or None) 
        if form.is_valid():
            dtinicial = str(form.cleaned_data['inicial'])
            dtfinal = str(form.cleaned_data['final'])
            idorigem = request.POST.get('filial_origem')
            iddestino = request.POST.get('filial_destino')
            return redirect('envios:pdfdatafilial',dtinicial=dtinicial, dtfinal=dtfinal,iddestino=iddestino,idorigem=idorigem) 
        else: 
            messages.error(request, "Formulário invalido!")  
            form = RelatorioDataFilialForm() 
    else: 
        form = RelatorioDataFilialForm()
    context = {
        'staff': is_staff(request.user),
        'form': form
    }    
    return render(request,template, context)

class PdfPorDataFilial(View):
    def get(self, request, dtinicial, dtfinal, iddestino, idorigem):
        titulo = 'Envios por data e filial'
        dtgeracao = datetime.now()
        lista = []
        origem = Lojas.object.get(id=idorigem)
        destino = Lojas.object.get(id=iddestino)
        # FORMATO DATA = ANO/MES/DIA
        #FILTRA OS ENVIOS PELA DATA DIGITADA
        envios = EnvioBh.object.filter(create_at__lte=dtfinal, create_at__gte=dtinicial,filial_destino=iddestino,filial_origem=idorigem)
        #PEGA OS ID DOS ENVIOS E FILTRA PELO MOVIMENTO PARA PEGAR OS EQUIPAMENTOS UTILIZADOS        
        for i in envios:
            lista.append(i.id)
        if not lista:
            return redirect('core:erro_relatorio')
        movimento = Movimento.object.filter(envio_id__in=lista)
        params = {
            'titulo': titulo,
            'envios': envios,
            'movimento': movimento,
            'dtgeracao': dtgeracao,
            'dtinicial': dtinicial,
            'dtfinal': dtfinal,
            'origem': origem,
            'destino': destino,
        }

        return Render.render('pdf_data_filial_envio.html', params)

class PdfEnviosPendentes(View):
    def get(self, request):
        titulo = 'Envios pendentes'
        dtgeracao = datetime.now()
        lista = []
        # FORMATO DATA = ANO/MES/DIA
        #FILTRA OS ENVIOS PELA DATA DIGITADA
        origem = list(request.user.profile.filiais.all().values_list('name', flat=True))
        envios = EnvioBh.object.filter(recebido=False, filial_origem__in=request.user.profile.filiais.all()).order_by('pk')
        #PEGA OS ID DOS ENVIOS E FILTRA PELO MOVIMENTO PARA PEGAR OS EQUIPAMENTOS UTILIZADOS        
        for i in envios:
            lista.append(i.id)
        if not lista:
            return redirect('core:erro_relatorio')
        movimento = Movimento.object.filter(envio__in=envios)
        params = {
            'titulo': titulo,
            'envios': envios,
            'movimento': movimento,
            'dtgeracao': dtgeracao,
            'origem':origem
        }

        return Render.render('pdf_pendentes_envio.html', params)


# ENVIO POR USUARIO        
def envio_por_usuario(request):
    template = 'viewporusuario.html'
    dtinicial = dtfinal = 0
    if request.method == 'POST':
        form = RelatorioUsuarioForm(request.POST)
        if form.is_valid():
            dtinicial = str(form.cleaned_data['inicial'])
            dtfinal = str(form.cleaned_data['final'])
            usuario = request.POST.get('usuario')
            return redirect('envios:pdfusuario',dtinicial=dtinicial, dtfinal=dtfinal, usuario=usuario) 
        else: 
            messages.error(request, "Formulário invalido!")
            form = RelatorioUsuarioForm()
    else: 
        form = RelatorioUsuarioForm()
    context = {
        'staff': is_staff(request.user),
        'form': form
    }    
    return render(request,template, context)

class PdfPorUsuario(View):
    def get(self, request, dtinicial, dtfinal, usuario):
        titulo = 'Envios por usuario'
        dtgeracao = datetime.now()
        lista = []
        usuario = User.objects.get(id=usuario)
        # FORMATO DATA = ANO/MES/DIA
        #FILTRA OS ENVIOS PELA DATA DIGITADA
        envios = EnvioBh.object.filter(create_at__lte=dtfinal, create_at__gte=dtinicial, user_id=usuario)
        #PEGA OS ID DOS ENVIOS E FILTRA PELO MOVIMENTO PARA PEGAR OS EQUIPAMENTOS UTILIZADOS
        for i in envios:
            lista.append(i.id)
        movimento = Movimento.object.filter(envio_id__in=lista)

        params = {
            'titulo': titulo,
            'envios': envios,
            'movimento': movimento,
            'dtgeracao': dtgeracao,
            'dtinicial': dtinicial,
            'dtfinal': dtfinal,
            'usuario': usuario,
        }

        return Render.render('pdf_usuario_envio.html', params)    

#FIM ENVIO POR USUARIO

# COMEÇO ENVIO POR MODELO

def envio_por_modelo(request):
    template = 'viewpormodelo.html'
    dtinicial = dtfinal = 0
    if request.method == 'POST':
        form = RelatorioDataModeloForm(request.POST or None) 
        if form.is_valid():
            dtinicial = str(form.cleaned_data['inicial'])
            dtfinal = str(form.cleaned_data['final'])
            modelo = request.POST.get('modelo')
            return redirect('envios:pdfdatamodelo',dtinicial=dtinicial, dtfinal=dtfinal,modelo=modelo) 
        else: 
            messages.error(request, "Formulário invalido!")  
            form = RelatorioDataModeloForm() 
    else: 
        form = RelatorioDataModeloForm()
    context = {
        'staff': is_staff(request.user),
        'form': form
    }    
    return render(request,template, context)

class PdfPorModelo(View):
    def get(self, request, dtinicial, dtfinal, modelo):
        titulo = 'Envios por data e filial'
        usuario = request.user
        dtgeracao = datetime.now()
        lista = []
        lista_equip = []
        # FORMATO DATA = ANO/MES/DIA
        #FILTRA OS ENVIOS PELA DATA DIGITADA
        envios = EnvioBh.object.filter(create_at__lte=dtfinal, create_at__gte=dtinicial)
        #PEGA OS ID DOS ENVIOS E FILTRA PELO MOVIMENTO PARA PEGAR OS EQUIPAMENTOS UTILIZADOS        
        for i in envios:
            lista.append(i.id)
        if not lista:
            return redirect('core:erro_relatorio')
        equip_id = Equipamento.object.filter(name__exact=modelo)
        for i in equip_id:
            lista_equip.append(i.id)
        movimento = Movimento.object.filter(envio_id__in=lista, equipamento_id__in=lista_equip)
        params = {
            'titulo': titulo,
            'envios': envios,
            'movimento': movimento,
            'dtgeracao': dtgeracao,
            'dtinicial': dtinicial,
            'dtfinal': dtfinal,
            'usuario':usuario,
        }

        return Render.render('pdf_data_modelo_envio.html', params)

#FIM ENVIO POR MODELO

# ____________________ PDF RECEBIMENTOS ___________________________

def recebimento_data(request):
    template = 'viewpordata_recebimento.html'
    dtinicial = dtfinal = 0
    if request.method == 'POST':
        form = RelatorioRecebDataForm(request.POST)
        if form.is_valid():
            dtinicial = str(form.cleaned_data['inicial'])
            dtfinal = str(form.cleaned_data['final'])
            return redirect('envios:pdfdata_receb',dtinicial=dtinicial, dtfinal=dtfinal) 
        else:
            messages.error(request, "Formulário invalido!")            
            form = RelatorioDataForm()
    else: 
        form = RelatorioDataForm()
    context = {
        'staff': is_staff(request.user),
        'form': form
    }    
    return render(request,template, context)
    

class PdfPorDataReceb(View):
    def get(self, request, dtinicial, dtfinal):
        titulo = 'Recebimentos por data'
        dtgeracao = datetime.now() 
        # FORMATO DATA = ANO/MES/DIA
        movimento = Recebimento.object.filter(create_at__lte=dtfinal, create_at__gte=dtinicial)
        #PEGA OS ID DOS ENVIOS E FILTRA PELO MOVIMENTO PARA PEGAR OS EQUIPAMENTOS UTILIZADOS

        params = {
            'titulo': titulo,
            'movimento': movimento,
            'dtgeracao': dtgeracao,
            'dtinicial': dtinicial,
            'dtfinal': dtfinal,
        }

        return Render.render('pdf_data_receb.html', params)


def recebimento_por_usuario(request):
    template = 'viewporusuario_recebimento.html'
    dtinicial = dtfinal = 0
    if request.method == 'POST':
        form = RelatorioUsuarioRecebForm(request.POST)
        if form.is_valid():
            dtinicial = str(form.cleaned_data['inicial'])
            dtfinal = str(form.cleaned_data['final'])
            usuario = request.POST.get('usuario')
            return redirect('envios:pdfusuario_receb',dtinicial=dtinicial, dtfinal=dtfinal, usuario=usuario) 
        else: 
            messages.error(request, "Formulário invalido!")
            form = RelatorioUsuarioForm()
    else: 
        form = RelatorioUsuarioForm()
    context = {
        'staff': is_staff(request.user),
        'form': form
    }    
    return render(request,template, context)

class PdfPorUsuarioReceb(View):
    def get(self, request, dtinicial, dtfinal, usuario):
        titulo = 'Recebimentos por usuario'
        dtgeracao = datetime.now()
        usuario = User.objects.get(id=usuario)
        movimento = Recebimento.object.filter(create_at__lte=dtfinal, create_at__gte=dtinicial, user_id=usuario)

        params = {
            'titulo': titulo,
            'movimento': movimento,
            'dtgeracao': dtgeracao,
            'dtinicial': dtinicial,
            'dtfinal': dtfinal,
            'usuario': usuario,
        }

        return Render.render('pdf_usuario_receb.html', params)    
