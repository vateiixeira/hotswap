from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Usuario
from my_project.atendimento.models import Atendimento


@login_required
def help_desk(request):
    template = 'helpdesk.html'
    user = request.user
    perfil = Usuario.objects.get(user = user)

    pendente = Atendimento.object.filter(status = 'p'  , setor = perfil.setor, loja = perfil.loja ).count()
    concluido = Atendimento.object.filter(status = 'r' , setor = perfil.setor, loja = perfil.loja ).count()
    cancelados = Atendimento.object.filter(status = 'o', setor = perfil.setor, loja = perfil.loja ).count()
    

    context = {
        'quantidade': {
            'pendente': pendente,
            'concluido': concluido,
            'cancelados': cancelados
        },
        'usuario': {
            'setor': perfil.setor,
            'loja' : perfil.loja,
            'id' : perfil.user.id
        }
    }
    
    return render(request,template, context)
