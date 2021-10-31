from rest_framework import serializers
from django.contrib.auth import get_user_model
from my_project.estoque.models import Equipamento,CategoriaHD,CategoriaMemoria,CategoriaProcessador,CategoriaSO

User = get_user_model()

class EquipamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipamento
        fields = ('__all__')

class EquipamentoListSerializer(EquipamentoSerializer):
    loja_info = serializers.CharField(source='loja.name')
    is_backup = serializers.SerializerMethodField()

    class Meta(EquipamentoSerializer.Meta):        
        fields = EquipamentoSerializer.Meta.fields

    def get_is_backup(self,obj):
        return 'Sim' if obj.backup else 'Nao'

class CategoriaHDSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaHD
        fields = ('__all__')

class CategoriaMemoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaMemoria
        fields = ('__all__')

class CategoriaProcessadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaProcessador
        fields = ('__all__')

class CategoriaSOSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaSO
        fields = ('__all__')