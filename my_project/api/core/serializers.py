from rest_framework import serializers
from django.contrib.auth import get_user_model
from my_project.core.models import Fornecedor, Lojas

User = get_user_model()

class LojasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lojas
        fields = ('__all__')

class FornecedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fornecedor
        fields = ('__all__')