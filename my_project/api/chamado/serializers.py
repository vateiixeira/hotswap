from rest_framework import serializers
from django.contrib.auth import get_user_model
from my_project.chamado.models import Chamado

User = get_user_model()

class ChamadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chamado
        fields = ('__all__')

class ChamadoListSerializer(ChamadoSerializer):
    status_info = serializers.SerializerMethodField()
    create_at = serializers.DateTimeField(format='%d/%m/%y')
    dt_finalizado_info = serializers.DateField(format='%d/%m/%y',source='dt_finalizado')
    loja_info = serializers.CharField(source='loja.name')
    
    class Meta(ChamadoSerializer.Meta):
        fields = ChamadoSerializer.Meta.fields

    def get_status_info(self,obj):
        return obj.chamado_verbose()