from django.db import models
from my_project.core.models import Lojas


class DataInauguracao(models.Model):
    cod_filial = models.IntegerField()
    loja = models.CharField(max_length=20)
    inauguracao = models.CharField(max_length=20)


class TestDataInauguracao(models.Model):
    cod_filial = models.IntegerField()
    loja = models.CharField(max_length=20)
    inauguracao = models.CharField(max_length=20)


class CircuitoDados(models.Model):
    nome_filial = models.CharField(max_length=20)
    cod_filial = models.CharField(max_length=20, null=True)
    faixa_ip = models.CharField(max_length=20, null=True)
    produto = models.CharField(max_length=20)
    circuito = models.CharField(max_length=20)
    roteador = models.CharField(max_length=20, null=True)
    velocidade = models.CharField(max_length=10, null=True)
    

class CircuitoVoz(models.Model):
    regiao_filial = models.CharField(max_length=20)
    operadora = models.CharField(max_length=20)
    designacao = models.CharField(max_length=50)
    servico_equipamento = models.CharField(max_length=80,null=True)
    tel_abrir_chamado = models.CharField(max_length=30, null=True)
    op_urla = models.CharField(max_length=50,null=True)


class CentralTelefonica(models.Model):
    modelo = models.CharField(max_length=50)
    end_ip = models.CharField(max_length=20)
    qtd_ramais = models.IntegerField()
    qtd_ramais_utilizados = models.IntegerField()
    dt_ult_preventiva = models.DateField(null=True)
    filial = models.ForeignKey(Lojas, on_delete = 'CASCADE')
    obs = models.CharField(max_length=400, null=True)


class HistoricoIncidente(models.Model):
    incidente = models.CharField(max_length=400)
    data = models.DateTimeField()
    filial = models.ForeignKey(Lojas, on_delete='CASCADE')
