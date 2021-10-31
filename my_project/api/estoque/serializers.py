from rest_framework import serializers
from django.contrib.auth import get_user_model
from my_project.estoque.models import Movimento,Equipamento
from my_project.envios.models import EnvioBh

User = get_user_model()

class MovimentoEnvioSerializer(serializers.ModelSerializer):
    serial = serializers.CharField(source='equipamento.serial')
    patrimonio = serializers.CharField(source='equipamento.patrimonio')
    class Meta:
        model = Movimento
        exclude = ('envio',)


class EnvioSerializer(serializers.ModelSerializer):
    movimento = MovimentoEnvioSerializer(many=True)
    class Meta:
        model = EnvioBh
        exclude = ('recebido',)

    def create(self, validated_data):
        movimento_data = validated_data.pop('movimento')
        envio = EnvioBh.object.create(**validated_data)
        movimento_list = []
        for i in movimento_data:
            o = Movimento.object.create(envio=envio, **i)
            movimento_list.append(o)


        loja_destino = envio.filial_destino
        loja_origem = envio.filial_origem
        for item in movimento_list:
            id_equipamento = item.equipamento_id
            quantidade = item.quantidade                
            estoque = Equipamento.object.get(id=id_equipamento)                
            qtd_atual = estoque.qtd
            if estoque.loja == loja_destino:
                qtd_final = qtd_atual + quantidade
                estoque.qtd = qtd_final
                estoque.save()

            elif estoque.loja == loja_origem:
                qtd_final = qtd_atual - quantidade
                estoque.qtd = qtd_final
                estoque.save()
        
        return envio


class EnvioListSerializer(serializers.ModelSerializer):
    create_at = serializers.DateTimeField(format='%d/%m/%y')
    filial_origem = serializers.CharField(source='filial_origem.name')
    filial_destino = serializers.CharField(source='filial_origem.name')
    user = serializers.CharField(source='user.username')
    
    class Meta:
        model = EnvioBh
        fields = ('__all__')