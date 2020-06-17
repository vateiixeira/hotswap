from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, viewsets
from django.contrib.auth.models import User
from django.middleware.csrf import get_token
from my_project.envios.models import EnvioBh
from .serializers import Envio_Serializer, UsuarioHelpDeskSerializer,AtendimentoSerializer
from rest_framework.decorators import api_view
from my_project.helpdesk.models import Usuario
import json
from my_project.atendimento.models import Atendimento
from my_project.core.models import Lojas

class Envio_List(viewsets.ModelViewSet):
    queryset = EnvioBh.object.all()
    serializer_class = Envio_Serializer

@api_view()
def user_helpdesk(request,id):
    obj = User.objects.get(id = id)
    user = Usuario.objects.get(user = obj)
    serializer = UsuarioHelpDeskSerializer(user)
    return Response(serializer.data)

@api_view(['POST'])
def novo_atendimento_helpdesk(request):
    data = json.loads(request.body.decode('utf-8'))
    obj = Atendimento()
    obj.problema = data['problema']
    obj.setor = data['setor']
    obj.solicitante = data['solicitante']
    user = User.objects.get(id = data['user'])
    obj.user = user
    loja = Lojas.object.get(id = data['loja'])
    obj.loja = loja
    obj.save()
    print(data)
    return Response('ok')

@api_view(['GET'])
def list_atendimento_helpdesk(request):
    loja = Lojas.object.get(id = request.GET.get('loja'))
    if request.GET.get('setor') == 'GERENCIA':
        atendimento = Atendimento.object.filter(loja = loja)
        serializer = AtendimentoSerializer(atendimento, many=True)
    else:
        atendimento = Atendimento.object.filter(setor = request.GET.get('setor'), loja = loja)
        serializer = AtendimentoSerializer(atendimento, many=True)
    return Response(serializer.data)





