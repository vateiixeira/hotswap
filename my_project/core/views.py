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
from my_project.core.models import Profile
import mysql.connector
from mysql.connector import Error
from my_project.atendimento.models import Atendimento
from .conexao_oracle import conecta
from django.contrib.auth.models import User
from my_project.msg.models import Group_Msg
from my_project.atendimento.views import lista_id_bh, lista_id_moc
from django.core import serializers
from django.db.models import Sum

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

    #pega localidade do operador logado
    query_localidade = Profile.objects.get(user = request.user)
    if query_localidade.grupo == 'BH':
        see_bh = 1
    elif query_localidade.grupo == 'MONTES CLAROS' :
        see_bh = 2
    else:
        see_bh = 0

    # mensagens não lidas
    msg_nao_lida = Msg.object.filter(lida=False, dest=user).count()

    # envios pendentes
    envios_pendentes = EnvioBh.object.filter(recebido=False, filial_origem__in=request.user.profile.filiais.all()).count()

    #lista filiais
    lista_filial = []
    query_filial = Lojas.object.all()
    for i in query_filial:
        lista_filial.append(i.id)



    # lista filiais bh
    lojas_bh = []
    query_bh = Lojas.object.exclude(cidade='MONTES CLAROS')
    for i in query_bh:
        lojas_bh.append(i.id)

    
    data_atendimento_filial = contagem_atendimento_filial(request)
    filiais_data_atendimento_filial = list(Lojas.object.filter(polo='MONTES CLAROS').order_by('id').values_list('name',flat=True))
    
    data_atendimento_bh = contagem_atendimento_bh(request)
    filiais_data_atendimento_bh = list(Lojas.object.filter(polo='BH').order_by('id').values_list('name',flat=True))
    
    limit_contagem_atendimentos_moc = data_atendimento_filial[0]
    contagem_chamados_anual_moc = contagem_chamados_anual(request)
    data = contagem_chamados_anual_bh(request)
    #data_filial = contagem_chamados_filial()
    chamados = Chamado.object.filter(status=Chamado.STATUS_CHAMADO_PENDENTE, loja__name__in = filiais_data_atendimento_filial).count()
    chamados_bh = Chamado.object.filter(status=Chamado.STATUS_CHAMADO_PENDENTE, loja__name__in = filiais_data_atendimento_bh).count()
   
    # nao usa
    #mes_envios = contagem_envios_mes()
    atendimento_pendente = Atendimento.object.filter(status='p', loja__name__in = filiais_data_atendimento_filial).count()
    
    atendimento_pendente_bh = Atendimento.object.filter(status='p', loja__name__in = filiais_data_atendimento_bh).count()
    
    custo_chamado = custo_chamado_mensal(request)
    custo_chamado_bh = custo_chamado_mensal_bh(request)
    custo_chamado_anual_moc = custo_chamados_anual_moc(request)
    custo_chamado_anual_bh = custo_chamados_anual_bh(request)

    seus_atendimentos_pendentes = Atendimento.object.filter(responsavel=request.user,  status='p').count()
    
    context = {
        'lojas_bh': lojas_bh,
        'see_bh': see_bh,
        'staff': is_staff(user),
        'id': id_user,
        #'data_filial': data_filial,
        'contagem_chamados_anual_moc': contagem_chamados_anual_moc,      
        'data': data,      
        'user': user,
        'chamados': chamados,
        'chamados_bh': chamados_bh,
        'custo_chamado':custo_chamado,
        'custo_chamado_bh':custo_chamado_bh,
        'form_atendi': form_atendi,
        'grupo_msg': grupo_msg,
        'id_msg': id_msg,
        'data_atendimento_filial':data_atendimento_filial,
        'filiais_data_atendimento_filial':filiais_data_atendimento_filial,
        'atendimento_pendente':atendimento_pendente,
        'atendimento_pendente_bh':atendimento_pendente_bh,
        'msg_nao_lida':msg_nao_lida,  
        'lista_filial': lista_filial, 
        'limit_contagem_atendimentos_moc': limit_contagem_atendimentos_moc,     
        'data_atendimento_bh': data_atendimento_bh,  
        'filiais_data_atendimento_bh': filiais_data_atendimento_bh,  
        'custo_chamados_anual_moc': custo_chamado_anual_moc,   
        'custo_chamados_anual_bh': custo_chamado_anual_bh,   
        'envios_pendentes': envios_pendentes,
        'seus_atendimentos_pendentes': seus_atendimentos_pendentes
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
            try:
                profile = Profile.objects.get(user = user)
                print(profile) 
            except Profile.DoesNotExist:
                return redirect('helpdesk:help_desk')
            else:
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
        script = "select count(*) from exp_imp_movimento where data_movimento= CURDATE() and situacao_movimento=1 and tipo_movimento=1;"
        cursor.execute(script) 
        for i in cursor:
            data = i[0]
    #now = datetime.now()
    #data = now.year, now.month, now.day, now.hour, now.minute, now.second

    return JsonResponse(data, safe=False)


def contagem_chamados_anual(request):
    dia,mes,ano = get_data_final_mes()
    janeiro = Chamado.object.filter(create_at__lte=f'{ano}-1-31', create_at__gte=f'{ano}-1-1', loja__in = request.user.profile.filiais.filter(polo='MONTES CLAROS')).count()
    fevereiro = Chamado.object.filter(create_at__lte=f'{ano}-2-28', create_at__gte=f'{ano}-2-1', loja__in = request.user.profile.filiais.filter(polo='MONTES CLAROS')).count()
    marco = Chamado.object.filter(create_at__lte=f'{ano}-3-31', create_at__gte=f'{ano}-3-1', loja__in = request.user.profile.filiais.filter(polo='MONTES CLAROS')).count()
    abril = Chamado.object.filter(create_at__lte=f'{ano}-4-30', create_at__gte=f'{ano}-4-1', loja__in = request.user.profile.filiais.filter(polo='MONTES CLAROS')).count()
    maio = Chamado.object.filter(create_at__lte=f'{ano}-5-31', create_at__gte=f'{ano}-5-1', loja__in = request.user.profile.filiais.filter(polo='MONTES CLAROS')).count()
    jun = Chamado.object.filter(create_at__lte=f'{ano}-6-30', create_at__gte=f'{ano}-6-1', loja__in = request.user.profile.filiais.filter(polo='MONTES CLAROS')).count()
    julho = Chamado.object.filter(create_at__lte=f'{ano}-7-31', create_at__gte=f'{ano}-7-1', loja__in = request.user.profile.filiais.filter(polo='MONTES CLAROS')).count()
    agosto = Chamado.object.filter(create_at__lte=f'{ano}-8-31', create_at__gte=f'{ano}-8-1', loja__in = request.user.profile.filiais.filter(polo='MONTES CLAROS')).count()
    setembro = Chamado.object.filter(create_at__lte=f'{ano}-9-30', create_at__gte=f'{ano}-9-1', loja__in = request.user.profile.filiais.filter(polo='MONTES CLAROS')).count()
    outubro = Chamado.object.filter(create_at__lte=f'{ano}-10-31', create_at__gte=f'{ano}-10-1', loja__in = request.user.profile.filiais.filter(polo='MONTES CLAROS')).count()
    novembro = Chamado.object.filter(create_at__lte=f'{ano}-11-30', create_at__gte=f'{ano}-11-1', loja__in = request.user.profile.filiais.filter(polo='MONTES CLAROS')).count()
    dezembro = Chamado.object.filter(create_at__lte=f'{ano}-12-31', create_at__gte=f'{ano}-12-1', loja__in = request.user.profile.filiais.filter(polo='MONTES CLAROS')).count()
    data = [janeiro , fevereiro, marco, abril, maio, jun, julho, agosto, setembro, outubro,novembro,dezembro]
    return data


def contagem_chamados_anual_bh(request):
    dia,mes,ano = get_data_final_mes()
    janeiro = Chamado.object.filter(create_at__lte=f'{ano}-1-31', create_at__gte=f'{ano}-1-1', loja__in = request.user.profile.filiais.filter(polo='BH')).count()
    fevereiro = Chamado.object.filter(create_at__lte=f'{ano}-2-28', create_at__gte=f'{ano}-2-1', loja__in = request.user.profile.filiais.filter(polo='BH')).count()
    marco = Chamado.object.filter(create_at__lte=f'{ano}-3-31', create_at__gte=f'{ano}-3-1', loja__in = request.user.profile.filiais.filter(polo='BH')).count()
    abril = Chamado.object.filter(create_at__lte=f'{ano}-4-30', create_at__gte=f'{ano}-4-1', loja__in = request.user.profile.filiais.filter(polo='BH')).count()
    maio = Chamado.object.filter(create_at__lte=f'{ano}-5-31', create_at__gte=f'{ano}-5-1', loja__in = request.user.profile.filiais.filter(polo='BH')).count()
    jun = Chamado.object.filter(create_at__lte=f'{ano}-6-30', create_at__gte=f'{ano}-6-1', loja__in = request.user.profile.filiais.filter(polo='BH')).count()
    julho = Chamado.object.filter(create_at__lte=f'{ano}-7-31', create_at__gte=f'{ano}-7-1', loja__in = request.user.profile.filiais.filter(polo='BH')).count()
    agosto = Chamado.object.filter(create_at__lte=f'{ano}-8-31', create_at__gte=f'{ano}-8-1', loja__in = request.user.profile.filiais.filter(polo='BH')).count()
    setembro = Chamado.object.filter(create_at__lte=f'{ano}-9-30', create_at__gte=f'{ano}-9-1', loja__in = request.user.profile.filiais.filter(polo='BH')).count()
    outubro = Chamado.object.filter(create_at__lte=f'{ano}-10-31', create_at__gte=f'{ano}-10-1', loja__in = request.user.profile.filiais.filter(polo='BH')).count()
    novembro = Chamado.object.filter(create_at__lte=f'{ano}-11-30', create_at__gte=f'{ano}-11-1', loja__in = request.user.profile.filiais.filter(polo='BH')).count()
    dezembro = Chamado.object.filter(create_at__lte=f'{ano}-12-31', create_at__gte=f'{ano}-12-1', loja__in = request.user.profile.filiais.filter(polo='BH')).count()
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

    
def contagem_atendimento_bh(request):
    dia,mes,ano = get_data_final_mes()
    lista_lojas = Lojas.object.filter(polo='BH').order_by('id')
    data = []
    for i in lista_lojas:
        valor = Atendimento.object.filter(create_at__lte=(f'{ano}-{mes}-{dia}'), create_at__gte=(f'{ano}-{mes}-1'),loja=i).count()
        data.append(valor)
    # pav10 = Atendimento.object.filter(create_at__lte=(f'{ano}-{mes}-{dia}'), create_at__gte=(f'{ano}-{mes}-1'),loja=10).count()
    # cd = Atendimento.object.filter(create_at__lte=(f'{ano}-{mes}-{dia}'), create_at__gte=(f'{ano}-{mes}-1'),loja=12).count()
    # cof= Atendimento.object.filter(create_at__lte=(f'{ano}-{mes}-{dia}'), create_at__gte=(f'{ano}-{mes}-1'),loja=13).count()
    # tito = Atendimento.object.filter(create_at__lte=(f'{ano}-{mes}-{dia}'), create_at__gte=(f'{ano}-{mes}-1'),loja=14).count()
    # jfora = Atendimento.object.filter(create_at__lte=(f'{ano}-{mes}-{dia}'), create_at__gte=(f'{ano}-{mes}-1'),loja=15).count()
    # vaz = Atendimento.object.filter(create_at__lte=(f'{ano}-{mes}-{dia}'), create_at__gte=(f'{ano}-{mes}-1'),loja=16).count()
    # ampa = Atendimento.object.filter(create_at__lte=(f'{ano}-{mes}-{dia}'), create_at__gte=(f'{ano}-{mes}-1'),loja=17).count()
    # hort = Atendimento.object.filter(create_at__lte=(f'{ano}-{mes}-{dia}'), create_at__gte=(f'{ano}-{mes}-1'),loja=18).count()
    # bridadeiro = Atendimento.object.filter(create_at__lte=(f'{ano}-{mes}-{dia}'), create_at__gte=(f'{ano}-{mes}-1'),loja=19).count()
    # divi = Atendimento.object.filter(create_at__lte=(f'{ano}-{mes}-{dia}'), create_at__gte=(f'{ano}-{mes}-1'),loja=20).count()
    # justin = Atendimento.object.filter(create_at__lte=(f'{ano}-{mes}-{dia}'), create_at__gte=(f'{ano}-{mes}-1'),loja=21).count()
    # p2 = Atendimento.object.filter(create_at__lte=(f'{ano}-{mes}-{dia}'), create_at__gte=(f'{ano}-{mes}-1'),loja=22).count()
    # jj = Atendimento.object.filter(create_at__lte=(f'{ano}-{mes}-{dia}'), create_at__gte=(f'{ano}-{mes}-1'),loja=23).count()
    # trop = Atendimento.object.filter(create_at__lte=(f'{ano}-{mes}-{dia}'), create_at__gte=(f'{ano}-{mes}-1'),loja=24).count()
    # serrano = Atendimento.object.filter(create_at__lte=(f'{ano}-{mes}-{dia}'), create_at__gte=(f'{ano}-{mes}-1'),loja=26).count()
    # hm = Atendimento.object.filter(create_at__lte=(f'{ano}-{mes}-{dia}'), create_at__gte=(f'{ano}-{mes}-1'),loja=27).count()
    # br040 = Atendimento.object.filter(create_at__lte=(f'{ano}-{mes}-{dia}'), create_at__gte=(f'{ano}-{mes}-1'),loja=28).count()
    # dctf = Atendimento.object.filter(create_at__lte=(f'{ano}-{mes}-{dia}'), create_at__gte=(f'{ano}-{mes}-1'),loja=29).count()
    # dcp2 = Atendimento.object.filter(create_at__lte=(f'{ano}-{mes}-{dia}'), create_at__gte=(f'{ano}-{mes}-1'),loja=30).count()
    # dcbg = Atendimento.object.filter(create_at__lte=(f'{ano}-{mes}-{dia}'), create_at__gte=(f'{ano}-{mes}-1'),loja=31).count()
    # sl = Atendimento.object.filter(create_at__lte=(f'{ano}-{mes}-{dia}'), create_at__gte=(f'{ano}-{mes}-1'),loja=32).count()
    # itabi = Atendimento.object.filter(create_at__lte=(f'{ano}-{mes}-{dia}'), create_at__gte=(f'{ano}-{mes}-1'),loja=33).count()
    # jatai = Atendimento.object.filter(create_at__lte=(f'{ano}-{mes}-{dia}'), create_at__gte=(f'{ano}-{mes}-1'),loja=34).count()
    # ipatinga = Atendimento.object.filter(create_at__lte=(f'{ano}-{mes}-{dia}'), create_at__gte=(f'{ano}-{mes}-1'),loja=35).count()
    return data

def contagem_atendimento_filial(request):
    dia,mes,ano = get_data_final_mes()
    lista_lojas = Lojas.object.filter(polo='MONTES CLAROS').order_by('id')
    data = []
    for i in lista_lojas:
        valor = Atendimento.object.filter(create_at__lte=(f'{ano}-{mes}-{dia}'), create_at__gte=(f'{ano}-{mes}-1'),loja=i).count()
        data.append(valor)
    # dulce = Atendimento.object.filter(create_at__lte=(f'{ano}-{mes}-{dia}'), create_at__gte=(f'{ano}-{mes}-1'),loja=2).count()
    # sion = Atendimento.object.filter(create_at__lte=(f'{ano}-{mes}-{dia}'), create_at__gte=(f'{ano}-{mes}-1'),loja=4).count()
    # jaragua = Atendimento.object.filter(create_at__lte=(f'{ano}-{mes}-{dia}'), create_at__gte=(f'{ano}-{mes}-1'),loja=7).count()
    # ceanorte = Atendimento.object.filter(create_at__lte=(f'{ano}-{mes}-{dia}'), create_at__gte=(f'{ano}-{mes}-1'),loja=3).count()
    # mangabeira = Atendimento.object.filter(create_at__lte=(f'{ano}-{mes}-{dia}'), create_at__gte=(f'{ano}-{mes}-1'),loja=6).count()
    # posto_dulce = Atendimento.object.filter(create_at__lte=(f'{ano}-{mes}-{dia}'), create_at__gte=(f'{ano}-{mes}-1'),loja=11).count()
    # posto_jg = Atendimento.object.filter(create_at__lte=(f'{ano}-{mes}-{dia}'), create_at__gte=(f'{ano}-{mes}-1'),loja=25).count()
    # dc_dulce = Atendimento.object.filter(create_at__lte=(f'{ano}-{mes}-{dia}'), create_at__gte=(f'{ano}-{mes}-1'),loja=9).count()
    # data = [dulce , sion , ceanorte , jaragua, mangabeira, posto_dulce, posto_jg, dc_dulce]
    return data

def custo_chamados_anual_moc(request):
    dia,mes,ano = get_data_final_mes()
    janeiro = Chamado.object.filter(updated_at__lte=f'{ano}-1-31', updated_at__gte=f'{ano}-1-1', loja__in = request.user.profile.filiais.filter(polo='MONTES CLAROS')).aggregate(Sum('valor'))
    fevereiro = Chamado.object.filter(updated_at__lte=f'{ano}-2-28', updated_at__gte=f'{ano}-2-1', loja__in = request.user.profile.filiais.filter(polo='MONTES CLAROS')).aggregate(Sum('valor'))
    marco = Chamado.object.filter(updated_at__lte=f'{ano}-3-31', updated_at__gte=f'{ano}-3-1', loja__in = request.user.profile.filiais.filter(polo='MONTES CLAROS')).aggregate(Sum('valor'))
    abril = Chamado.object.filter(updated_at__lte=f'{ano}-4-30', updated_at__gte=f'{ano}-4-1', loja__in = request.user.profile.filiais.filter(polo='MONTES CLAROS')).aggregate(Sum('valor'))
    maio = Chamado.object.filter(updated_at__lte=f'{ano}-5-31', updated_at__gte=f'{ano}-5-1', loja__in = request.user.profile.filiais.filter(polo='MONTES CLAROS')).aggregate(Sum('valor'))
    jun = Chamado.object.filter(updated_at__lte=f'{ano}-6-30', updated_at__gte=f'{ano}-6-1', loja__in = request.user.profile.filiais.filter(polo='MONTES CLAROS')).aggregate(Sum('valor'))
    julho = Chamado.object.filter(updated_at__lte=f'{ano}-7-31', updated_at__gte=f'{ano}-7-1', loja__in = request.user.profile.filiais.filter(polo='MONTES CLAROS')).aggregate(Sum('valor'))
    agosto = Chamado.object.filter(updated_at__lte=f'{ano}-8-31', updated_at__gte=f'{ano}-8-1', loja__in = request.user.profile.filiais.filter(polo='MONTES CLAROS')).aggregate(Sum('valor'))
    setembro = Chamado.object.filter(updated_at__lte=f'{ano}-9-30', updated_at__gte=f'{ano}-9-1', loja__in = request.user.profile.filiais.filter(polo='MONTES CLAROS')).aggregate(Sum('valor'))
    outubro = Chamado.object.filter(updated_at__lte=f'{ano}-10-31', updated_at__gte=f'{ano}-10-1', loja__in = request.user.profile.filiais.filter(polo='MONTES CLAROS')).aggregate(Sum('valor'))
    novembro = Chamado.object.filter(updated_at__lte=f'{ano}-11-30', updated_at__gte=f'{ano}-11-1', loja__in = request.user.profile.filiais.filter(polo='MONTES CLAROS')).aggregate(Sum('valor'))
    dezembro = Chamado.object.filter(updated_at__lte=f'{ano}-12-31', updated_at__gte=f'{ano}-12-1', loja__in = request.user.profile.filiais.filter(polo='MONTES CLAROS')).aggregate(Sum('valor'))
    data = [janeiro.get('valor__sum') , fevereiro.get('valor__sum'), marco.get('valor__sum'), abril.get('valor__sum'), 
            maio.get('valor__sum'), jun.get('valor__sum'), julho.get('valor__sum'), agosto.get('valor__sum'), 
            setembro.get('valor__sum'), outubro.get('valor__sum'),novembro.get('valor__sum'),dezembro.get('valor__sum')]
    # METODO GET PEGA O VALOR DA SOMA QUE FOI GERADO DENTRO DE UM DICT NA QUERY SET
    aux = []
    for i in data:
        if i is None:
            i = 0
            aux.append(i)
        else:
# ITEREAR OS VALORES GERADOS PARA TRATAR SE EH NONE E TAMBEM FAZER RETORNAR O FLOAT SE HOPUVER VALOR.. 
            valor = float(i)
            aux.append(valor)
    return aux

def custo_chamados_anual_bh(request):
    dia,mes,ano = get_data_final_mes()
    janeiro = Chamado.object.filter(updated_at__lte=f'{ano}-1-31', updated_at__gte=f'{ano}-1-1', loja__in = request.user.profile.filiais.filter(polo='BH')).aggregate(Sum('valor'))
    fevereiro = Chamado.object.filter(updated_at__lte=f'{ano}-2-28', updated_at__gte=f'{ano}-2-1', loja__in = request.user.profile.filiais.filter(polo='BH')).aggregate(Sum('valor'))
    marco = Chamado.object.filter(updated_at__lte=f'{ano}-3-31', updated_at__gte=f'{ano}-3-1', loja__in = request.user.profile.filiais.filter(polo='BH')).aggregate(Sum('valor'))
    abril = Chamado.object.filter(updated_at__lte=f'{ano}-4-30', updated_at__gte=f'{ano}-4-1', loja__in = request.user.profile.filiais.filter(polo='BH')).aggregate(Sum('valor'))
    maio = Chamado.object.filter(updated_at__lte=f'{ano}-5-31', updated_at__gte=f'{ano}-5-1', loja__in = request.user.profile.filiais.filter(polo='BH')).aggregate(Sum('valor'))
    jun = Chamado.object.filter(updated_at__lte=f'{ano}-6-30', updated_at__gte=f'{ano}-6-1', loja__in = request.user.profile.filiais.filter(polo='BH')).aggregate(Sum('valor'))
    julho = Chamado.object.filter(updated_at__lte=f'{ano}-7-31', updated_at__gte=f'{ano}-7-1', loja__in = request.user.profile.filiais.filter(polo='BH')).aggregate(Sum('valor'))
    agosto = Chamado.object.filter(updated_at__lte=f'{ano}-8-31', updated_at__gte=f'{ano}-8-1', loja__in = request.user.profile.filiais.filter(polo='BH')).aggregate(Sum('valor'))
    setembro = Chamado.object.filter(updated_at__lte=f'{ano}-9-30', updated_at__gte=f'{ano}-9-1', loja__in = request.user.profile.filiais.filter(polo='BH')).aggregate(Sum('valor'))
    outubro = Chamado.object.filter(updated_at__lte=f'{ano}-10-31', updated_at__gte=f'{ano}-10-1', loja__in = request.user.profile.filiais.filter(polo='BH')).aggregate(Sum('valor'))
    novembro = Chamado.object.filter(updated_at__lte=f'{ano}-11-30', updated_at__gte=f'{ano}-11-1', loja__in = request.user.profile.filiais.filter(polo='BH')).aggregate(Sum('valor'))
    dezembro = Chamado.object.filter(updated_at__lte=f'{ano}-12-31', updated_at__gte=f'{ano}-12-1', loja__in = request.user.profile.filiais.filter(polo='BH')).aggregate(Sum('valor'))
    data = [janeiro.get('valor__sum') , fevereiro.get('valor__sum'), marco.get('valor__sum'), abril.get('valor__sum'), 
            maio.get('valor__sum'), jun.get('valor__sum'), julho.get('valor__sum'), agosto.get('valor__sum'), 
            setembro.get('valor__sum'), outubro.get('valor__sum'),novembro.get('valor__sum'),dezembro.get('valor__sum')]
    # METODO GET PEGA O VALOR DA SOMA QUE FOI GERADO DENTRO DE UM DICT NA QUERY SET
    aux = []
    for i in data:
        if i is None:
            i = 0
            aux.append(i)
        else:
    # ITEREAR OS VALORES GERADOS PARA TRATAR SE EH NONE E TAMBEM FAZER RETORNAR O FLOAT SE HOPUVER VALOR.. 
            valor = float(i)
            aux.append(valor)
    return aux

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

def custo_chamado_mensal(request):
    chamado_custo = 0
    dia,mes,ano = get_data_final_mes()
    result = Chamado.object.filter(dt_finalizado__lte=(f'{ano}-{mes}-{dia}'), dt_finalizado__gte=(f'{ano}-{mes}-1'), loja__in = request.user.profile.filiais.filter(polo='MONTES CLAROS'))
    # ser
    if not result:
        chamado_custo = 0
    for i in result:        
        chamado_custo = chamado_custo + i.valor
    return chamado_custo

def custo_chamado_mensal_bh(request):
    chamado_custo = 0
    dia,mes,ano = get_data_final_mes()
    result = Chamado.object.filter(dt_finalizado__lte=(f'{ano}-{mes}-{dia}'), dt_finalizado__gte=(f'{ano}-{mes}-1'), loja_id__in = request.user.profile.filiais.filter(polo='BH'))
    if not result:
        chamado_custo = 0
    for i in result:        
        chamado_custo = chamado_custo + i.valor
    return chamado_custo

def atendimento_pendente_def(request):
    data = Atendimento.object.filter(status='p', loja_id__in = lista_id_moc).count()
    return data

def atendimento_pendente_def_bh(request):
    data = Atendimento.object.filter(status='p', loja_id__in = lista_id_bh).count()
    return data
