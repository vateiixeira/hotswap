from django.db import models
from my_project.estoque.models import Equipamento
from my_project.core.models import Lojas
from django.contrib.auth.models import User

class Transferencia(models.Model):
    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE)
    destino = models.ForeignKey(Lojas,related_name='transf_destino', on_delete=models.CASCADE)
    obs = models.CharField('Observações', max_length=300) 
    qtd = models.IntegerField('Quantidade')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    create_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
        

    object = models.Manager()    

    class Meta:
        verbose_name = "Transferência"
        verbose_name_plural = "Transferências"
        ordering = ['-create_at']


