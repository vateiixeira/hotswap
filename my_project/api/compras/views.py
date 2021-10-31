from rest_framework import viewsets
from django.http import Http404
from my_project.api.compras.filters import ComprasFilterBackend

from my_project.compras.models import Compras
from .serializers import *

class ComprasViewset(viewsets.ModelViewSet):
    serializer_class = ComprasSerializer
    filter_backends = [ComprasFilterBackend]
    queryset = Compras.objects.all()

    def get_queryset(self):
        return Compras.objects.filter(filial__in=self.request.user.profile.filiais.all())

    def get_serializer_class(self):
        if self.action == 'list':
            return ComprasListSerializer
        return ComprasSerializer