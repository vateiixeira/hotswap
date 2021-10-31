from rest_framework import serializers
from django.contrib.auth import get_user_model
from my_project.atendimento.models import Atendimento

User = get_user_model()

class AtendimentoListSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()
    responsavel_info = serializers.SerializerMethodField()
    create_at_info = serializers.DateTimeField(format='%d/%m/%y',source='create_at')
    updated_at_info = serializers.DateTimeField(format='%d/%m/%y', source='updated_at')
    status_info = serializers.SerializerMethodField()
    loja_info = serializers.CharField(source='loja.name')

    class Meta:
        model = Atendimento
        exclude = ('setor_visualiza_solucao',)

    def get_user_info(self,obj):
        if obj.user:
            return obj.user.username
        return ''
    def get_responsavel_info(self,obj):
        if obj.responsavel:
            return obj.responsavel.username
        return ''

    def get_status_info(self,obj):
        return obj.status_verbose()

class AtendimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atendimento
        exclude = ('setor_visualiza_solucao',)