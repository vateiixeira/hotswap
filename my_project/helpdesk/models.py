from django.db import models
from django.contrib.auth.models import User
from my_project.estoque.models import Equipamento
from my_project.core.models import Lojas

class Usuario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    setor = models.CharField("Setor", max_length=50, choices= Equipamento.SETOR_CHOICES)
    loja = models.ForeignKey(Lojas, verbose_name="Filial", on_delete=models.CASCADE)
    
    create_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return str(self.user)