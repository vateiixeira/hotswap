from rest_framework import serializers
from django.contrib.auth import get_user_model
from my_project.compras.models import Compras
from my_project.transf.models import Transferencia
from ..equipamento.serializers import EquipamentoListSerializer

User = get_user_model()

class ComprasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compras
        fields = ('__all__')

class ComprasListSerializer(ComprasSerializer):
    user = serializers.PrimaryKeyRelatedField(source='user.username', allow_null=True,read_only=True)
    fornecedor = serializers.PrimaryKeyRelatedField(source='fornecedor.name', allow_null=True,read_only=True)
    filial = serializers.CharField(source='filial.name')
    equipamento = EquipamentoListSerializer()
    create_at = serializers.DateTimeField(format='%d/%m/%y')
    updated_at = serializers.DateTimeField(format='%d/%m/%y')
    
    class Meta(ComprasSerializer.Meta):
        fields = ComprasSerializer.Meta.fields
        