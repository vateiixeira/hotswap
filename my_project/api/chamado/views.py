from rest_framework.decorators import api_view
from rest_framework.response import Response
from my_project.api.chamado.filters import ChamadoFilterBackend
from my_project.chamado.models import Chamado
from rest_framework import viewsets
from django.http import Http404
from .serializers import *


class ChamadoViewset(viewsets.ModelViewSet):
    filter_backends = [ChamadoFilterBackend]

    def get_serializer_class(self):
        if self.action == 'list':
            return ChamadoListSerializer
        return ChamadoSerializer

    def get_queryset(self):
        queryset = Chamado.object.all()

        queryset = queryset.filter(loja__in=self.request.user.profile.filiais.all())

        return queryset

    def partial_update(self, request, *args, **kwargs):
        super().partial_update(request, *args, **kwargs)
        obj = self.get_object()
        serializer = ChamadoListSerializer(obj)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        obj = self.get_object()
        serializer = ChamadoListSerializer(obj)
        return Response(serializer.data)

@api_view(['GET'])
def lista_status_chamados(request):
    status = Chamado.STATUS_CHAMADO_CHOICES
    data = [{
        'id': i[0],
        'value': i[1]
    } for i in status]
    return Response(data)