from django.db import models
from my_project.core.models import Lojas
from django.contrib.auth.models import User


class Chamado(models.Model):
    SIT_CHOICE = [
        ("p", "PENDENTE"),
        ("r", "RESOLVIDO")
    ]

    chamado = models.IntegerField('Número chamado')   
    modelo = models.CharField('Modelo', max_length=50)
    serial = models.CharField("Serial",max_length=100)
    loja = models.ForeignKey(Lojas,on_delete=models.CASCADE) 
    create_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantidade = models.IntegerField('Quantidade', default=1)
    defeito = models.CharField("Defeito", max_length=200)
    valor = models.DecimalField('Valor', max_digits=7, decimal_places=2, blank=True)
    status = models.CharField(max_length=1, choices=SIT_CHOICE, default='p')
    dt_finalizado = models.DateField(verbose_name='Data Finalizado', null=True)

    # status True = chamado não resolvido

    object = models.Manager()

    def __str__(self):
        return self.defeito

    class Meta:
        verbose_name = "Chamado"
        verbose_name_plural = "Chamados"
        ordering = ['-create_at']


    


