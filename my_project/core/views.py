from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from my_project.chamado.models import Chamado
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from my_project.estoque.models import Equipamento
from datetime import datetime
from calendar import monthrange
from my_project.envios.models import EnvioBh
from my_project.atendimento.views import add_atendimento
from my_project.atendimento.forms import AtendimentoForm
from my_project.msg.models import Group_Msg, Msg
from my_project.core.utils import is_staff
import mysql.connector
from mysql.connector import Error
from my_project.atendimento.models import Atendimento
from .conexao_oracle import conecta
from django.contrib.auth.models import User
from my_project.msg.models import Group_Msg

@login_required
def homepage(request):
    template = 'index.html'
    user = request.user
    id_user = user.id

    # adiciona atendimento
    form_atendi = AtendimentoForm()
    add_atendimento(request,user)

    #pega dados do usuario para direcionar em mensagens    
    grupo_msg = str(Group_Msg.object.get(user_id=user.id))
    id_msg = user.id

    # mensagens não lidas
    msg_nao_lida = Msg.object.filter(lida=False, dest=user).count()

    #lista filiais
    lista_filial = []
    query_filial = Lojas.object.all()
    for i in query_filial:
        lista_filial.append(i.name)

    atendimento_pendente = atendimento_pendente_def()
    data_atendimento_filial = contagem_atendimento_filial()
    limit_contagem_atendimentos_moc = data_atendimento_filial[0]
    data = contagem_chamados_anual()
    data_filial = contagem_chamados_filial()
    chamados = Chamado.object.filter(status='p').count()
    mes_envios = contagem_envios_mes()
    custo_chamado = custo_chamado_mensal()
    context = {
        'staff': is_staff(user),
        'id': id_user,
        'data_filial': data_filial,
        'data': data,      
        'user': user,
        'chamados': chamados,
        'mes_envios': mes_envios,
        'custo_chamado':custo_chamado,
        'form_atendi': form_atendi,
        'grupo_msg': grupo_msg,
        'id_msg': id_msg,
        'data_atendimento_filial':data_atendimento_filial,
        'atendimento_pendente':atendimento_pendente,
        'msg_nao_lida':msg_nao_lida,  
        'lista_filial': lista_filial, 
        'limit_contagem_atendimentos_moc': limit_contagem_atendimentos_moc,     
    }
    
    return render(request,template,context)
  
def logout_request(request):
    logout(request)
    messages.info(request, "Logout feito!")
    return redirect("core:homepage")

def register(request):
    if request.method == 'POST':
        instancia_profile = Profile()  
        grupo_msg = Group_Msg()      
        form = CriarUsuarioForm(request.POST) 
        form_profile = ProfileForm(request.POST)       
        if form.is_valid():            
            user = form.save()
            user.set_password(user.password)
            user.save()
            
            form_profile.save(commit=False)

            instancia = User.objects.get(username = form.cleaned_data['username'])
            instancia_profile.grupo = form_profile.cleaned_data['grupo']
            instancia_profile.user = instancia

            grupo_msg.user = instancia
            grupo_msg.grupo = 'membro'
            if form_profile.is_valid():
                instancia_profile.save()
                grupo_msg.save()
                messages.error(request,'Conta criada com sucesso!')                
            else:
                messages.error(request,'Formulário inválido!')
        else:            
            messages.error(request,'Formulário inválido!')
    else:
        form_profile = ProfileForm(request.POST)
        form = CriarUsuarioForm(request.POST)
    template='register.html'
    context = {
        'form_profile': form_profile,
        'message': messages,
    }
    return render(request,template,context)

def sessao_oracle(request):
    template = 'lista_sessao_bloqueada.html'
    data = sessao_travada()    
    context = {
        'data': data,
    }
    return render(request,template,context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!            
            return redirect('core:homepage')

        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'changepassword.html', {
        'form': form
    })

def login_request(request):
    template = 'login.html'
    if request.method == 'POST':    
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(request, username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('core:homepage')
        else:
            messages.error(request, f'Você digitou usuario/senha inválidos.')
    context = {
        'message': messages
    }
    return render(request,template, context)

@login_required
def loja(request):
    template = 'lojas.html'
    form = LojasForm(request.POST or None)
    if form.is_valid() and request.method =='POST':
        count_lojas = Lojas.object.all().count()
        if count_lojas == 7:
            messages.error(request, 'Sistema limitado apenas as filiais de Montes Claros. \n LOJA NÃO CADASTRADA!! ')
        else:
            form.save()
            return redirect('core:homepage')
    else:
        print('FUDEUS')
    context = {
        'form': form
    }
    return render(request,template,context)

#CADASTRO DE FORNECEDORES
@login_required
def fornecedores(request):
    template = 'cadastro_fornecedores.html'

    if request.method == 'POST':
        form = FornecedoresForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('core:homepage')
    else:
        form = FornecedoresForm()
        messages.error(request, f'Formulário inválido, revise os campos digitados.')
    
    context = {
        'form': form,
    }
    return render(request,template,context)


def erro_relatorio(request):
    template= 'erro_relatorio.html'
    return render(request,template)

def get_modelo(request):
    modelo = request.GET.get('modelo', None)
    data = {
        'modelo': modelo,
        'is_taken': Equipamento.object.filter(modelo__iexact=modelo).exists()
    }  
    return JsonResponse(data)

def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)

def sessao_travada():
    query = conecta()
    return query

def notas_travadas_mysql(request):
    if request.method == 'GET':
        cnx = mysql.connector.connect(user='econect', password='123456',
                                host='192.168.3.123',
                                database='concentrador')
        cursor = cnx.cursor()
        script = "select count(*) from exp_imp_movimento where data_movimento= CURDATE() and situacao_movimento=1;"
        cursor.execute(script) 
        for i in cursor:
            data = i[0]
    #now = datetime.now()
    #data = now.year, now.month, now.day, now.hour, now.minute, now.second

    return JsonResponse(data, safe=False)


def contagem_chamados_anual():
    dia,mes,ano = get_data_final_mes()
    janeiro = Chamado.object.filter(create_at__lte=f'{ano}-1-31', create_at__gte=f'{ano}-1-1').count()
    fevereiro = Chamado.object.filter(create_at__lte=f'{ano}-2-28', create_at__gte=f'{ano}-2-1').count()
    marco = Chamado.object.filter(create_at__lte=f'{ano}-3-31', create_at__gte=f'{ano}-3-1').count()
    abril = Chamado.object.filter(create_at__lte=f'{ano}-4-30', create_at__gte=f'{ano}-4-1').count()
    maio = Chamado.object.filter(create_at__lte=f'{ano}-5-31', create_at__gte=f'{ano}-5-1').count()
    jun = Chamado.object.filter(create_at__lte=f'{ano}-6-30', create_at__gte=f'{ano}-6-1').count()
    julho = Chamado.object.filter(create_at__lte=f'{ano}-7-31', create_at__gte=f'{ano}-7-1').count()
    agosto = Chamado.object.filter(create_at__lte=f'{ano}-8-31', create_at__gte=f'{ano}-8-1').count()
    setembro = Chamado.object.filter(create_at__lte=f'{ano}-9-30', create_at__gte=f'{ano}-9-1').count()
    outubro = Chamado.object.filter(create_at__lte=f'{ano}-10-31', create_at__gte=f'{ano}-10-1').count()
    novembro = Chamado.object.filter(create_at__lte=f'{ano}-11-30', create_at__gte=f'{ano}-11-1').count()
    dezembro = Chamado.object.filter(create_at__lte=f'{ano}-12-31', create_at__gte=f'{ano}-12-1').count()
    data = [janeiro , fevereiro, marco, abril, maio, jun, julho, agosto, setembro, outubro,novembro,dezembro]
    return data

def contagem_chamados_filial():
    dia,mes,ano = get_data_final_mes()
    dulce = Chamado.object.filter(create_at__lte=f'{ano}-12-31', create_at__gte=f'{ano}-1-1', loja=2).count()
    sion = Chamado.object.filter(create_at__lte=f'{ano}-12-31', create_at__gte=f'{ano}-1-1', loja=4).count()
    jaragua = Chamado.object.filter(create_at__lte=f'{ano}-12-31', create_at__gte=f'{ano}-1-1', loja=7).count()
    ceanorte = Chamado.object.filter(create_at__lte=f'{ano}-12-31', create_at__gte=f'{ano}-1-1', loja=3).count()
    mangabeira = Chamado.object.filter(create_at__lte=f'{ano}-12-31', create_at__gte=f'{ano}-1-1', loja=6).count()
    data_filial = [dulce , sion , jaragua , ceanorte, mangabeira]
    return data_filial

def contagem_atendimento_filial():
    dia,mes,ano = get_data_final_mes()
    dulce = Atendimento.object.filter(create_at__lte=(f'{ano}-{mes}-{dia}'), create_at__gte=(f'{ano}-{mes}-1'),loja=2).count()
    sion = Atendimento.object.filter(create_at__lte=(f'{ano}-{mes}-{dia}'), create_at__gte=(f'{ano}-{mes}-1'),loja=4).count()
    jaragua = Atendimento.object.filter(create_at__lte=(f'{ano}-{mes}-{dia}'), create_at__gte=(f'{ano}-{mes}-1'),loja=7).count()
    ceanorte = Atendimento.object.filter(create_at__lte=(f'{ano}-{mes}-{dia}'), create_at__gte=(f'{ano}-{mes}-1'),loja=3).count()
    mangabeira = Atendimento.object.filter(create_at__lte=(f'{ano}-{mes}-{dia}'), create_at__gte=(f'{ano}-{mes}-1'),loja=6).count()
    data = [dulce , sion , ceanorte , jaragua, mangabeira]
    return data

def get_data_final_mes():
    mes = datetime.now().month
    ano = datetime.now().year
    tamanho = monthrange(ano, mes)
    dia = tamanho[1]
    return dia,mes,ano

def contagem_envios_mes():
    dia,mes,ano = get_data_final_mes()
    mes_envios = EnvioBh.object.filter(create_at__lte=(f'{ano}-{mes}-{dia}'), create_at__gte=(f'{ano}-{mes}-1')).count()
    return mes_envios

def custo_chamado_mensal():
    chamado_custo = 0
    dia,mes,ano = get_data_final_mes()
    result = Chamado.object.filter(create_at__lte=(f'{ano}-{mes}-{dia}'), create_at__gte=(f'{ano}-{mes}-1'))
    if not result:
        chamado_custo = 0
    for i in result:        
        chamado_custo = chamado_custo + i.valor
    return chamado_custo

def atendimento_pendente_def():
    data = Atendimento.object.filter(status='p').count()
    return data
