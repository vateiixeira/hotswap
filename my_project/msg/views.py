from django.shortcuts import render
from .forms import MsgForm
from django.contrib.auth.models import User
from .models import Msg, Group_Msg
from django.contrib import messages
from django.db.models import Q
from my_project.core.utils import is_staff


def cadastro(request):
    template = 'cad_msg.html'
    form = MsgForm(request.POST or None)
    model = Msg()
    user = request.user

    if request.method == "POST":
        if form.is_valid():
            model.user = user
            model.dest = form.cleaned_data['dest']
            model.assunto = form.cleaned_data['assunto']
            model.mensagem = form.cleaned_data['mensagem']
            model.grupo = form.cleaned_data['grupo']
            model.geral = form.cleaned_data['geral']
            model.importancia = form.cleaned_data['importancia']
            model.save()
            messages.success(request,'Mensagem enviada!')
        else:
            messages.error(request,'Erro ao enviar mensagem! Valide os campos preenchidos.')
    else:
        form = MsgForm()
    context = {
        'staff': is_staff(request.user),
        'form': form
    }       
    return render(request,template,context)

def msg(request,id,grupo):

    # SINTAXE REVERSA PARA FUNCIONAR NA HOMEPAGE.. NAO FAÇO IDEIA PQ PRECISA TER OS DADOS AQUI, RS
    def pega_dados_msg():
        user = request.user
        id_user = user.id
        #pega dados do usuario para direcionar em mensagens
        grupo_msg = str(Group_Msg.object.get(user_id=id_user))
        id_msg = user.id
        return id_msg,grupo_msg

    pega_dados = pega_dados_msg()
    id_msg = pega_dados[0]
    grupo_msg = pega_dados[1]

    # QUERYSET PARA PEGAR MENSAGEM DE CADA PRODUTO
    msg = Msg.object.filter(Q(geral=True) & Q(grupo=grupo) | Q(dest_id=id)).order_by('-create_at')
    
    context = {
        'staff': is_staff(request.user),
        'msg': msg,
        'grupo_msg': grupo_msg,
        'id_msg': id_msg,
    }
    template = 'msg.html'
    return render(request,template,context)

def msg_indi(request,id):
    user = request.user
    msg = Msg.object.get(id=id)

    # SINTAXE REVERSA PARA FUNCIONAR NA HOMEPAGE.. NAO FAÇO IDEIA PQ PRECISA TER OS DADOS AQUI, RS
    def pega_dados_msg():
        user = request.user
        id_user = user.id
        #pega dados do usuario para direcionar em mensagens
        grupo_msg = str(Group_Msg.object.get(user_id=id_user))
        id_msg = user.id
        return id_msg,grupo_msg

    pega_dados = pega_dados_msg()
    id_msg = pega_dados[0]
    grupo_msg = pega_dados[1]

    # SALVA SE A MENSAGEM FOI LIDA
    msg.lida = True
    msg.save()

    # verifica se é o criador da mensagem
    def if_owner():
        if user.id == msg.user_id:
            return True
        else:
            return False

    context = {
        'staff': is_staff(request.user),
        'msg':msg,
        'owner': if_owner(),
        'grupo_msg': grupo_msg,
        'id_msg': id_msg,
    }
    template = 'msg_ind.html'
    return render(request,template,context)