from rest_framework import serializers
from my_project.envios.models import EnvioBh
from my_project.helpdesk.models import Usuario
from my_project.atendimento.models import Atendimento


class Envio_Serializer(serializers.ModelSerializer):
    filial_origem = serializers.StringRelatedField(many=False)
    filial_destino = serializers.StringRelatedField(many=False)
    user = serializers.StringRelatedField(many=False)
    create_at = serializers.DateTimeField(format='%d/%m/%Y')
    class Meta:
        model = EnvioBh
        fields = '__all__'

class UsuarioHelpDeskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class AtendimentoSerializer(serializers.ModelSerializer):
    user_finaliza = serializers.StringRelatedField()
    class Meta:
        model = Atendimento
        fields = '__all__'