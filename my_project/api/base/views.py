from rest_framework import viewsets
from django.http import Http404

from my_project.api.transf.filters import TransferenciaFilterBackend
from .serializers import *
from my_project.transf.models import Transferencia

class DataInauguracaoViewset(viewsets.ModelViewSet):
    serializer_class = DataInauguracaoSerializer
    #filter_backends = [DataInauguracaoFilterBackend]

    def get_serializer_class(self):
        if self.action == 'list':
            pass
            #return DataInauguracaoListSerializer
        return DataInauguracaoSerializer

    def get_queryset(self):
        queryset = DataInauguracao.objects.all()

        return queryset

class CircuitoDadosViewset(viewsets.ModelViewSet):
    serializer_class = CircuitoDadosSerializer
    #filter_backends = [CircuitoDadosFilterBackend]

    def get_serializer_class(self):
        if self.action == 'list':
            pass
            #return CircuitoDadosListSerializer
        return CircuitoDadosSerializer

    def get_queryset(self):
        queryset = CircuitoDados.objects.all()

        return queryset

class CircuitoVozViewset(viewsets.ModelViewSet):
    serializer_class = CircuitoVozSerializer
    #filter_backends = [CircuitoVozFilterBackend]

    def get_serializer_class(self):
        if self.action == 'list':
            pass
            #return CircuitoVozListSerializer
        return CircuitoVozSerializer

    def get_queryset(self):
        queryset = CircuitoVoz.objects.all()

        return queryset

class CentralTelefonicaViewset(viewsets.ModelViewSet):
    serializer_class = CentralTelefonicaSerializer
    #filter_backends = [CentralTelefonicaFilterBackend]

    def get_serializer_class(self):
        if self.action == 'list':
            pass
            #return CentralTelefonicaListSerializer
        return CentralTelefonicaSerializer

    def get_queryset(self):
        queryset = CentralTelefonica.objects.all()

        return queryset

class HistoricoIncidenteViewset(viewsets.ModelViewSet):
    serializer_class = HistoricoIncidenteSerializer 
    #filter_backends = [HistoricoIncidenteFilterBackend]

    def get_serializer_class(self):
        if self.action == 'list':
            pass
            #return HistoricoIncidenteListSerializer
        return HistoricoIncidenteSerializer

    def get_queryset(self):
        queryset = HistoricoIncidente.objects.all()

        queryset = queryset.filter(filial__in=self.request.user.profile.filiais.all())

        return queryset

class IpFixoViewset(viewsets.ModelViewSet):
    serializer_class = IpFixoSerializer
    #filter_backends = [IpFixoFilterBackend]

    def get_serializer_class(self):
        if self.action == 'list':
            pass
            #return IpFixoListSerializer
        return IpFixoSerializer

    def get_queryset(self):
        queryset = IpFixo.objects.all()

        return queryset

class FeriasViewset(viewsets.ModelViewSet):
    serializer_class = FeriasSerializer
    #filter_backends = [FeriasFilterBackend]

    def get_serializer_class(self):
        if self.action == 'list':
            pass
            #return FeriasListSerializer
        return FeriasSerializer

    def get_queryset(self):
        queryset = Ferias.objects.all()

        return queryset