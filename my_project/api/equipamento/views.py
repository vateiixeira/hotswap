from rest_framework import viewsets
from django.http import Http404
from rest_framework.response import Response
from .serializers import EquipamentoSerializer
from my_project.estoque.models import Equipamento,CategoriaHD,CategoriaMemoria,CategoriaProcessador,CategoriaSO
from .serializers import *
from .filter import EquipamentoFilterBackend

class EquipamentoViewset(viewsets.ModelViewSet):
    filter_backends = [EquipamentoFilterBackend]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return EquipamentoListSerializer

        return EquipamentoSerializer

    
    def get_queryset(self):
        queryset = Equipamento.object.all()

        queryset = queryset.filter(loja__in=self.request.user.profile.filiais.all())
        
        return queryset

    def partial_update(self, request, *args, **kwargs):
        super().partial_update(request, *args, **kwargs)
        obj = self.get_object()
        serializer = EquipamentoListSerializer(obj)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        obj = self.get_object()
        serializer = EquipamentoListSerializer(obj)
        return Response(serializer.data)

        
    
class CategoriaHDViewset(viewsets.ModelViewSet):
    queryset = CategoriaHD.object.all()
    serializer_class = CategoriaHDSerializer

class CategoriaMemoriaViewset(viewsets.ModelViewSet):
    queryset = CategoriaMemoria.object.all()
    serializer_class = CategoriaMemoriaSerializer

class CategoriaProcessadorViewset(viewsets.ModelViewSet):
    queryset = CategoriaProcessador.object.all()
    serializer_class = CategoriaProcessadorSerializer

class CategoriaSOViewset(viewsets.ModelViewSet):
    queryset = CategoriaSO.object.all()
    serializer_class = CategoriaSOSerializer
