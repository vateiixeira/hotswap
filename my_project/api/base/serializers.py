from rest_framework import serializers
from django.contrib.auth import get_user_model
from my_project.base.models import DataInauguracao,CircuitoDados,CircuitoVoz,CentralTelefonica,HistoricoIncidente,IpFixo,Ferias
from ..equipamento.serializers import EquipamentoListSerializer

User = get_user_model()

class DataInauguracaoSerializer(serializers.ModelSerializer):
    data_inauguracao_info = serializers.DateField(format='%d/%m/%y', source='data_inauguracao',read_only=True)
    class Meta:
        model = DataInauguracao
        fields = ('__all__')

class CircuitoDadosSerializer(serializers.ModelSerializer):
    class Meta:
        model = CircuitoDados
        fields = ('__all__')

class CircuitoVozSerializer(serializers.ModelSerializer):
    class Meta:
        model = CircuitoVoz
        fields = ('__all__')

class CentralTelefonicaSerializer(serializers.ModelSerializer):
    #dt_ult_preventiva = serializers.DateField(format='%d/%m/%y')
    filial_name = serializers.CharField(source='filial.name')
    class Meta:
        model = CentralTelefonica
        fields = ('__all__')

class HistoricoIncidenteSerializer(serializers.ModelSerializer):
    data_info = serializers.DateTimeField(format='%d/%m/%y %H:%M:%S', source='data',read_only=True)
    filial_name = serializers.CharField(source='filial.name',read_only=True)
    class Meta:
        model = HistoricoIncidente
        fields = ('__all__')

class IpFixoSerializer(serializers.ModelSerializer):
    filial_name = serializers.CharField(source='filial.name')
    class Meta:
        model = IpFixo
        fields = ('__all__')

class FeriasSerializer(serializers.ModelSerializer):
    inicio = serializers.DateField(format='%d/%m/%y')
    termino = serializers.DateField(format='%d/%m/%y')
    
    class Meta:
        model = Ferias
        fields = ('__all__')

