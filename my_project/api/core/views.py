from django.utils import timezone
from rest_framework import viewsets
from django.http import Http404
from my_project.api.core.utils import get_data_year_atendimento, get_data_year_chamado
from my_project.atendimento.models import Atendimento
from my_project.chamado.models import Chamado
from my_project.core.dates import replace_day
from my_project.core.models import GRUPO_USUARIOS, GRUPO_USUARIOS_BH, GRUPO_USUARIOS_GERAL, GRUPO_USUARIOS_MOC, Lojas, Fornecedor
from my_project.core.views import contagem_chamados_anual, contagem_chamados_anual_bh, custo_chamado_mensal, custo_chamado_mensal_bh, custo_chamados_anual_bh, custo_chamados_anual_moc, get_data_final_mes
from .serializers import *
from rest_framework.decorators import action
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from my_project.envios.models import EnvioBh

class LojasViewset(viewsets.ModelViewSet):
    queryset = Lojas.object.all()
    serializer_class = LojasSerializer



class FornecedorViewset(viewsets.ModelViewSet):
    queryset = Fornecedor.object.all()
    serializer_class = FornecedorSerializer


class DashboardView(APIView):

    #authentication_classes = [authentication.TokenAuthentication]
    #permission_classes = [permissions.IsAdminUser]


    def get(self,request,*args,**kwargs):

        # filiais liberadas
        lojas = self.request.user.profile.filiais.all()
        user = self.request.user
        polo = self.request.user.profile.grupo

        filiais_bh = lojas.filter(polo=GRUPO_USUARIOS_BH)
        filiais_moc = lojas.filter(polo=GRUPO_USUARIOS_MOC)

        now =timezone.now()
        last_date_month = replace_day(now,31)
        
        # atendimentos
        atendimentos_pendentes = str(Atendimento.object.filter(loja__in=lojas,status='p').count())
        seus_atendimentos_pendentes = str(Atendimento.object.filter(loja__in=lojas,status='p',responsavel=user).count())
        
        # ranking atendimentos bh
        list_filiais_grafico_bh = list(Lojas.object.filter(id__in=lojas,polo=GRUPO_USUARIOS_BH).values_list('name',flat=True))
        list_filiais_grafico_bh_id = list(Lojas.object.filter(id__in=lojas,polo=GRUPO_USUARIOS_BH).values_list('id',flat=True))
        show_fico_bh = True if len(list_filiais_grafico_bh) > 0 else False
        #data_grafico_bh = get_data_year_atendimento(filiais_bh)
        data_grafico_bh = [
            Atendimento.object.filter(create_at__date__lte=last_date_month, create_at__gte=now.replace(day=1), loja_id=x).count() for x in list_filiais_grafico_bh_id
        ]
        ranking_atendimentos_bh = {
            'show': show_fico_bh,
            'filiais': list_filiais_grafico_bh,
            'data': data_grafico_bh
        }
        # ranking atendimentos moc
        list_filiais_grafico_moc = list(Lojas.object.filter(id__in=lojas,polo=GRUPO_USUARIOS_MOC).values_list('name',flat=True))
        list_filiais_grafico_moc_id = list(Lojas.object.filter(id__in=lojas,polo=GRUPO_USUARIOS_MOC).values_list('id',flat=True))
        show_fico_moc = True if len(list_filiais_grafico_moc) > 0 else False
        data_grafico_moc = [
            Atendimento.object.filter(create_at__date__lte=last_date_month, create_at__gte=now.replace(day=1), loja_id=x).count() for x in list_filiais_grafico_moc_id
        ]
        # alterar funcao para pegar ateneimtneot
        ranking_atendimentos_moc = {
            'show': show_fico_moc,
            'filiais': list_filiais_grafico_moc,
            'data': data_grafico_moc
        }

        # chamados
        chamados_pendentes = str(Chamado.object.filter(loja__in=lojas,status=Chamado.STATUS_CHAMADO_PENDENTE).count())
        envios_pendentes = str(EnvioBh.object.filter(filial_destino__in=lojas,recebido=False).count())
        chamados_custo_moc = custo_chamado_mensal(request)
        chamados_custo_bh = custo_chamado_mensal_bh(request)
        
        # grafico custo 
        # moc
        data_grafico_custo_moc = custo_chamados_anual_moc(request)
        list_filiais_grafico_moc = list(Lojas.object.filter(id__in=lojas).values_list('name',flat=True))
        ranking_chamados_custo_moc = {
            'show': show_fico_moc,
            'filiais': list_filiais_grafico_moc,
            'data': data_grafico_custo_moc
        }


        data_grafico_qtd_moc = contagem_chamados_anual(request)
        ranking_chamados_qtd_moc = {
            'show': show_fico_moc,
            'filiais': list_filiais_grafico_moc,
            'data': data_grafico_qtd_moc
        }

        # bh
        data_grafico_custo_bh = custo_chamados_anual_bh(request)
        list_filiais_grafico_bh = list(Lojas.object.filter(id__in=lojas).values_list('name',flat=True))
        ranking_chamados_custo_bh = {
            'show': show_fico_bh,
            'filiais': list_filiais_grafico_bh,
            'data': data_grafico_custo_bh
        }

        data_grafico_qtd_bh = contagem_chamados_anual_bh(request)
        ranking_chamados_qtd_bh = {
            'show': show_fico_bh,
            'filiais': list_filiais_grafico_bh,
            'data': data_grafico_qtd_bh
        }        

        data = {
            'atendimentos_pendentes': atendimentos_pendentes,
            'seus_atendimentos_pendentes': seus_atendimentos_pendentes,
            'ranking_atendimentos_bh': ranking_atendimentos_bh,
            'ranking_atendimentos_moc': ranking_atendimentos_moc,
            'custo_chamado_mensal_card': f"MOC:${chamados_custo_moc} | BH:${chamados_custo_bh}",
            'chamados_pendentes': chamados_pendentes,
            'envios_pendentes': envios_pendentes,
            'ranking_chamados_custo_moc': ranking_chamados_custo_moc,
            'ranking_chamados_custo_bh': ranking_chamados_custo_bh,
            'ranking_chamados_qtd_bh': ranking_chamados_qtd_bh,
            'ranking_chamados_qtd_moc': ranking_chamados_qtd_moc,
            'show_bh':show_fico_bh,
            'show_moc':show_fico_moc

        }
        return Response(data,status=status.HTTP_200_OK)