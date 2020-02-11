from django.db import models
from my_project.core.models import Lojas, Fornecedor
from my_project.estoque.models import Equipamento
from django.contrib.auth.models import User
from django import forms

STATUS_MANUTENCAO = (
    ('CORRETIVA', 'CORRETIVA'),
    ('PREVENTIVA', 'PREVENTIVA'),
    ('MAU USO', 'MAU USO')
)


class Compras(models.Model):
    num_pedido =    models.IntegerField('Numero pedido', null=True, blank=True)
    filial =        models.ForeignKey(Lojas,on_delete=models.CASCADE)
    fornecedor =    models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
    dt_vencimento = models.DateField('Data Vencimento', null=True, blank=True)
    equipamento =   models.ForeignKey(Equipamento, on_delete=models.CASCADE)
    obs =           models.CharField('Observações', null=True, blank=True, max_length=455)
    user =          models.ForeignKey(User, on_delete=models.CASCADE)

    create_at =     models.DateTimeField('Criado em', auto_now_add=True)
    updated_at =    models.DateTimeField('Atualizado em', auto_now=True)    


    objects = models.Manager()


    def __str__(self):
        return str(self.num_pedido)

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"


class Manutencao_Mensal(models.Model):
    dt_entrega = models.CharField('Mes da entrega', max_length= 30)
    fornecedor =    models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
    filial =        models.ForeignKey(Lojas,on_delete=models.CASCADE)
    conta = models.IntegerField('Conta', blank=True, null=True) 
    descricao = models.TextField('Descricao', max_length=400, null=True)
    valor = models.FloatField('Valor')
    nf =  models.IntegerField('Nota Fiscal')
    ordem = models.IntegerField('Num Ordem')
    vencimento = models.DateField('Vencimento')
    status = models.CharField('Status', choices=STATUS_MANUTENCAO, max_length=20)
    dt_aquisicao_equipamento = models.DateField('Data Aquisicao', null=True, blank=True)
    dt_ultima_manutencao = models.DateField('Data Ultima Manutencao', null=True, blank=True)

    objects = models.Manager()


    def __str__(self):
        return str(f'{self.filial} | {self.dt_entrega} | {self.vencimento}')

    class Meta:
        verbose_name = "Manutencao Mensal"
        verbose_name_plural = "Manutencoes Mensais"


