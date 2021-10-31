from django import http
from rest_framework import viewsets
from django.http import Http404
from rest_framework.response import Response
from my_project.api.estoque.filters import EnvioFilterBackend
from my_project.estoque.models import Movimento
from my_project.envios.models import EnvioBh
from .serializers import *
from rest_framework.decorators import action
from rest_framework import status

class EnvioViewset(viewsets.ModelViewSet):
    serializer_class = EnvioSerializer
    filter_backends = [EnvioFilterBackend]

    def get_serializer_class(self):
        if self.action == 'list':
            return EnvioListSerializer
        return EnvioSerializer
    
    def get_queryset(self):
        queryset = EnvioBh.object.all().order_by('-id')

        queryset = queryset.filter(filial_origem__in=self.request.user.profile.filiais.all())

        return queryset

    def partial_update(self, request, *args, **kwargs):
        super().partial_update(request, *args, **kwargs)
        obj = self.get_object()
        serializer = EnvioListSerializer(obj)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        obj = self.get_object()
        serializer = EnvioListSerializer(obj)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        envio = self.get_object()
        for movimento in Movimento.object.filter(envio=envio):
            loja_destino = envio.filial_destino
            loja_origem = envio.filial_origem
            quantidade = movimento.quantidade   
            equipamento = movimento.equipamento
            qtd_atual = equipamento.qtd
            if equipamento.loja == loja_destino:
                qtd_final = qtd_atual - quantidade
                equipamento.qtd = qtd_final
                equipamento.save()

            elif equipamento.loja == loja_origem:
                qtd_final = qtd_atual + quantidade
                equipamento.qtd = qtd_final
                equipamento.save()

        return super().destroy(request, *args, **kwargs)

    @action(methods=['get'], detail=True)
    def receber(self,request,*args,**kwargs):
        obj = self.get_object()
        obj.recebido = True
        obj.save()
        return Response({'ok': True},status=status.HTTP_200_OK)
        

