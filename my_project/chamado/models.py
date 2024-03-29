from my_project.estoque.models import Equipamento
from django.db import models
from my_project.core.models import Fornecedor, Lojas
from django.contrib.auth.models import User


class Chamado(models.Model):
    SIT_CHOICE = [
        ("p", "PENDENTE"),
        ("r", "RESOLVIDO"),
        ("c", "COMPRADO"),
        ("o", "RECOLHIDO"),
    ]
    STATUS_CHAMADO_CORRETIVO = 'corretivo'
    STATUS_CHAMADO_MAUUSO = 'mau-uso'
    STATUS_CHAMADO_AQUISICAO = 'aquisicao'
    STATUS_CHAMADO_PENDENTE = 'pendente'

    STATUS_CHAMADO_CHOICES = (
        (STATUS_CHAMADO_CORRETIVO, 'Corretivo'),
        (STATUS_CHAMADO_MAUUSO, 'Mau uso'),
        (STATUS_CHAMADO_AQUISICAO, 'Aquisição'),
        (STATUS_CHAMADO_PENDENTE, 'Pendente'),
    )


    chamado = models.CharField('Número chamado',max_length=60)   
    modelo = models.CharField('Modelo', max_length=50)
    serial = models.CharField("Serial",max_length=100)
    equipamento = models.ForeignKey(Equipamento,on_delete=models.CASCADE,null=True,blank=True)
    loja = models.ForeignKey(Lojas,on_delete=models.CASCADE) 
    create_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantidade = models.IntegerField('Quantidade', default=1)
    defeito = models.TextField("Defeito",null=True,blank=True)
    valor = models.DecimalField('Valor', max_digits=7, decimal_places=2, blank=True)
    status = models.CharField(max_length=60, choices=STATUS_CHAMADO_CHOICES, default=STATUS_CHAMADO_PENDENTE)
    justificativa = models.TextField('Justificativa do chamado', null=True,blank=True)
    nfe = models.CharField('Nota Fiscal', max_length=60, null=True,blank=True)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, related_name='chamado', null=True,blank=True)
    dt_finalizado = models.DateField(verbose_name='Data Finalizado', null=True)

    # status True = chamado não resolvido
    def chamado_verbose(self):
        return dict(Chamado.STATUS_CHAMADO_CHOICES)[self.status]

    object = models.Manager()

    def __str__(self):
        return self.defeito

    class Meta:
        verbose_name = "Chamado"
        verbose_name_plural = "Chamados"
        ordering = ['-create_at']


    


