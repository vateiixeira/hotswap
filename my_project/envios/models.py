from django.db import models
from django.contrib.auth.models import User
from my_project.core.models import Lojas


class EnvioBh(models.Model):     
    filial_origem = models.ForeignKey(Lojas,related_name='origem',on_delete=models.CASCADE)
    filial_destino = models.ForeignKey(Lojas,on_delete=models.CASCADE)  
    num_nota = models.CharField('Número nota', max_length=10, null=True, blank=True)
    num_ficha_transf = models.CharField('Número ficha de transferência', max_length=10, null=True, blank=True)
    recebido = models.BooleanField('Recebido', default=False)
    #Recebido = True , Nao=False

    create_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)    
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    object = models.Manager() 

    def __str__(self):
        return str(self.id)


    class Meta:
        verbose_name = "Envio"
        verbose_name_plural = "Envios"
        

class Recebimento(models.Model):
    envio = models.ForeignKey(EnvioBh, related_name='recebimento',on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_at = models.DateTimeField('Recebido em', auto_now_add=True)

    object = models.Manager() 

    def __str__(self):
        return str(f'Nota: {self.envio.num_nota} | Envio:{self.envio}')

    class Meta:
        verbose_name = "Recebimento"
        verbose_name_plural = "Recebimentos"
