from rest_framework import serializers
from django.contrib.auth import get_user_model
from my_project.transf.models import Transferencia
from ..equipamento.serializers import EquipamentoListSerializer

User = get_user_model()

class TransferenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transferencia
        fields = ('__all__')

    def update(self, instance, validated_data):        
        equipamento = instance.equipamento
        equipamento.loja = instance.destino
        equipamento.save()

        return super().update(instance, validated_data)

    def create(self, validated_data):
        instance = super().create(validated_data)
        equipamento = instance.equipamento
        equipamento.loja = instance.destino
        equipamento.save()
        
        return instance

class TransferenciaListSerializer(TransferenciaSerializer):
    user_info = serializers.PrimaryKeyRelatedField(source='user.username', allow_null=True,read_only=True)
    destino_info = serializers.CharField(source='destino.name')
    equipamento = EquipamentoListSerializer()
    create_at = serializers.DateTimeField(format='%d/%m/%y')
    updated_at = serializers.DateTimeField(format='%d/%m/%y')
    
    class Meta(TransferenciaSerializer.Meta):
        fields = TransferenciaSerializer.Meta.fields
        