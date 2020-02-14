from rest_framework import serializers
from my_project.envios.models import EnvioBh


class Envio_Serializer(serializers.ModelSerializer):
    filial_origem = serializers.StringRelatedField(many=False)
    filial_destino = serializers.StringRelatedField(many=False)
    user = serializers.StringRelatedField(many=False)
    create_at = serializers.DateTimeField(format='%d/%m/%Y')
    class Meta:
        model = EnvioBh
        fields = '__all__'