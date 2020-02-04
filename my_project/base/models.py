from django.db import models
from my_project.core.models import Lojas

YESORNOT_CHOICES = (
    ('S', 'Sim'),
    ('N','Nao')
)


class DataInauguracao(models.Model):
    cod_filial = models.IntegerField()
    loja = models.CharField(max_length=20)
    inauguracao = models.CharField(max_length=20)
    
    def __str__(self):
        return self.loja


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
    operadora = models.CharField(max_length=100)
    designacao = models.CharField(max_length=200)
    servico_equipamento = models.CharField(max_length=200,null=True)
    tel_abrir_chamado = models.CharField(max_length=30, null=True)
    op_urla = models.CharField(max_length=50,null=True)
    


class CentralTelefonica(models.Model):
    modelo = models.CharField('Modelo',max_length=50)
    end_ip = models.CharField('End. IP',max_length=20)
    qtd_ramais = models.IntegerField('Quantidade de ramais')
    qtd_ramais_utilizados = models.IntegerField('Quantidade de ramais utilizados')
    dt_ult_preventiva = models.DateField('Data ultima preventiva',null=True)
    filial = models.ForeignKey(Lojas, on_delete = 'CASCADE')
    obs = models.CharField(max_length=400, null=True)

    
    def __str__(self):
        return str(self.filial)


class HistoricoIncidente(models.Model):
    incidente = models.CharField(max_length=400)
    data = models.DateTimeField()
    filial = models.ForeignKey(Lojas, on_delete='CASCADE')

class IpFixo(models.Model):
    filial = models.ForeignKey(Lojas, on_delete = 'CASCADE')
    ip_interno = models.CharField('Ip interno', max_length = 25)
    porta_interna = models.IntegerField('Porta Interna')
    ip_externo = models.CharField('Ip externo', max_length = 25)
    porta_externa = models.IntegerField('Porta Ixterna')
    status_online = models.CharField('Status do servico', max_length=20, choices = YESORNOT_CHOICES)

    def __str__(self):
        return str(self.filial)

class Ferias(models.Model):
    filial = models.ForeignKey(Lojas, on_delete = 'CASCADE')
    colaborador = models.CharField(max_length=50)
    mes = models.IntegerField('Mes')
    ano = models.IntegerField('Ano')
    inicio = models.DateField()
    termino = models.DateField()
    dias = models.IntegerField()
    decimo_terceiro = models.CharField('Decimo Terceiro', max_length=20, choices = YESORNOT_CHOICES)

    def __str__(self):
        return self.colaborador
    