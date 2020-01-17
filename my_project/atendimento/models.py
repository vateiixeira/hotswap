from django.db import models
from django.contrib.auth.models import User
from my_project.chamado.models import Chamado
from my_project.core.models import Lojas
from my_project.estoque.models import Equipamento


class Atendimento(models.Model):
    problema = models.CharField("Problema", max_length=455)
    solucao = models.CharField("Resolução", max_length=455, blank=True)
    status = models.CharField(max_length=1, choices=Chamado.SIT_CHOICE, default='p')
    setor = models.CharField("Setor", max_length=50, choices= Equipamento.SETOR_CHOICES)
    solicitante = models.CharField("Solicitante", max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    loja = models.ForeignKey(Lojas, verbose_name="Filial", on_delete=models.CASCADE)
    user_finaliza = models.ForeignKey(User, related_name='finalizado_user', on_delete=models.CASCADE, null=True, blank=True)

    create_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = "Atendimento"
        verbose_name_plural = "Atendimentos"

    object = models.Manager()