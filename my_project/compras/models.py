from django.db import models
from my_project.core.models import Lojas, Fornecedor
from my_project.estoque.models import Equipamento
from django.contrib.auth.models import User
from django import forms



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

    class Main:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"