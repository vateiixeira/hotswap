from rest_framework import viewsets
from django.http import Http404
from rest_framework.response import Response

from my_project.api.transf.filters import TransferenciaFilterBackend
from .serializers import *
from my_project.transf.models import Transferencia

class TransferenciaViewset(viewsets.ModelViewSet):
    filter_backends = [TransferenciaFilterBackend]

    def get_serializer_class(self):
        if self.action == 'list':
            return TransferenciaListSerializer
        return TransferenciaSerializer

    def get_queryset(self):
        queryset = Transferencia.object.all().order_by('-id')

        return queryset

    def partial_update(self, request, *args, **kwargs):
        super().partial_update(request, *args, **kwargs)
        obj = self.get_object()
        serializer = TransferenciaListSerializer(obj)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        obj = self.get_object()
        serializer = TransferenciaListSerializer(obj)
        return Response(serializer.data)