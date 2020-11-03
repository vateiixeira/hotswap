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
from my_project.chamado.models import Chamado

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
    data = request.data
    obj = Atendimento()
    obj.problema = data['problema']
    obj.setor = data['setor']
    obj.solicitante = data['solicitante']
    user = User.objects.get(id = data['user'])
    obj.user = user
    loja = Lojas.object.get(id = data['loja'])
    obj.loja = loja
    obj.save()
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

@api_view(['GET'])
def change_date(request):
    template = 'change_date.html'
    lista_chamados_antigos = [526188,526187,525761,525759,525719,525697,525634,525124,524927,524927,529222,527494,526415,532364,530578,530574,524927,534515,536543,536348,534577,534577,534576,534576,534575,534575,541172,541132,541131,538219,537889,537416,537416,534577,542772,542772,542771,542771,542757,541522,547527,547228,546508,546504,546500,553209,553062,550728,557152,557064,556555,556335,556334,555855,555583,555576,555575,555572,555570,555569,554672,554304,560465,560258,558848,556335,556335,566238,566237,566210,566208,566207,566206,566205,566204,566203,564958,564847,564266,563379,563267,563262,562998,562882,562453,570676,567981,567274,567274,483416,482623,484749,484715,491452,491187,497503,495488,495002,503922,503518,503517,503063,502588,502124,502123,502003,509618,514077,516431,515573,522283,520654,519380,453326,452730,454876,458655,457304,458655,472877,476233,474709,478778,573995,573863,573603,572295,579065,579063,579061,579050,579042,579040,579039,579027,579024,579023,576923,576783,576778,576777,576775,576773,583577,583005,582303,581965,580437,591409,588669,595780,595777,593681,593006,601175,599382,599008,598645,606136,606128,602454,602450,616877,616865,615074,614870,614374,612789,621617,619445]
    lista_nova = [
        526188,526187,525761,525759,525719,525697,525634,525124,524927,524927,529222,527494,526415,532364,530578,530574,524927,534515,536543,536348,534577,534577,534576,534576,534575,534575,541172,541132,541131,538219,537889,537416,537416,534577,542772,542772,542771,542771,542757,541522,547527,547228,546508,546504,546500,553209,553062,550728,557152,557064,556555,556335,556334,555855,555583,555576,555575,555572,555570,555569,554672,554304,560465,560258,558848,556335,556335,566238,566237,566210,566208,566207,566206,566205,566204,566203,564958,564847,564266,563379,563267,563262,562998,562882,562453,570676,567981,567274,567274,483416,482623,484749,484715,491452,491187,497503,495488,495002,503922,503518,503517,503063,502588,502124,502123,502003,509618,514077,516431,515573,522283,520654,519380,453326,452730,454876,458655,457304,458655,472877,476233,474709,478778,573995,573863,573603,572295,579065,579063,579061,579050,579042,579040,579039,579027,579024,579023,576923,576783,576778,576777,576775,576773,583577,583005,582303,581965,580437,591409,588669,595780,595777,593681,593006,601175,599382,599008,598645,606136,606128,602454,602450,616877,616865,615074,614870,614374,612789,621617,619445,
        472880,
        472882,
        472904,
        472884,
        514661,
        515245,
        519157,
        519158,
        520218,
        523191,
        524537,
        525717,
        526189,
        526349,
        526993,
        527875,
        530530,
        532158,
        532692,
        532359,
        556228,
        539412,
        539583,
        541030,
        543354,
        555249,
        556227,
        556225,
        556224,
        556220,
        556228,
        556221,
        556879,
        556878,
        556226,
        558224,
        472890,
        472922,
        5680252,
        623715,
        582007,
        582490,
        585094,
        585255,
        585807,
        586410,
        596540,
        603431,
        610500,
        602521,
        622056,
        622502,
        622719,
        623867,
        12456,
        626957,
        624951,
    ]
    try:
        objeto = Chamado.object.filter(chamado__in = lista_nova)
        print(objeto)
    except Chamado.DoesNotExist:
        return Response('NÃO EXISTE')
    else:
        for x in objeto:
            print(x.create_at)
            finalizado = x.dt_finalizado
            print(finalizado)
            x.create_at = f'{finalizado} 03:00:00.000200'
            x.save()
        return Response('ok')





