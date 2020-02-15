from django.db import models
from my_project.core.models import Lojas
from django.contrib.auth.models import User
from django.forms import ModelForm
from my_project.envios.models import EnvioBh


class Equipamento(models.Model):
    SETOR_CHOICES=(
        ("FRENTE CAIXA", "Frente de caixa"),
        ("RECEPCAO", "Recepção"),
        ("SALAO", "Salao"),
        ("PERECIVEIS", "Perecíveis"),
        ("GERENCIA", "Gerência"),
        ("TESOURARIA", "Tesouraria"),
        ("SEGURANCA", "Segurança"),
        ("RM", "Rm"),
        ("RM FISCAL", "Rm Fiscal"),
        ("CONTABILIDADE", "Contabilidade"),
        ("RH", "Rh"),
        ("ACOUGUE", "Açougue"),
        ("TREINAMENTO", "Treinamento"),
        ("SOE", "Soe"),
        ("ALMOXARIFADO", "Almoxarifado"),
        ("CPD", "CPD"),
        ("CALLCENTER", "Callcenter"),
        ("COMERCIAL", "Comercial"),
        ("PRECIFICACAO", "Precificação"),
        ("PADARIA", "Padaria"),
        ("MANUTENCAO", "Manutenção"),
        ("HORTIFRUTI", "Hortifruti"),
        ("CREDITO", "Crédito"),
        ("ENCARREGADOS", "Encarregados"),
        ("ALMOXARIFADO", "Almoxarifado"),
        ("RESTAURANTE", "Restaurante"),
        ("SND", "SND"),
        ("GERAL", "Geral"),
        ("POSTO-PISTA", "Posto-Pista"),
        ("POSTO-ADM", "Posto-Adm"),

    )
    name = models.CharField("Nome", max_length=50)
    modelo = models.CharField("Modelo", max_length=50)
    serial = models.CharField("Serial", max_length=100)
    patrimonio = models.CharField("Patrimônio",max_length=100)
    # se for backup retorna true
    backup = models.BooleanField("Backup?", default = False)
    setor = models.CharField("Setor", max_length=50, choices= SETOR_CHOICES)
    loja = models.ForeignKey(Lojas, on_delete=models.CASCADE, verbose_name='Loja', default=1)
    create_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    qtd = models.IntegerField('Estoque', default=0)
    obs = models.TextField()
    #image = models.ImageField(upload_to='courses/images', verbose_name='Imagem', null=True, blank=True)
    #user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.patrimonio)

    class Meta:
        verbose_name = "Equipamento"
        verbose_name_plural = "Equipamentos"

    object = models.Manager()
    

class Movimento(models.Model):
    TIPO_CHOICE= (
        ("s", "Saída"),
        ("e", "Entrada")
    )
    equipamento = models.ForeignKey(Equipamento,on_delete=models.CASCADE)    
    envio = models.ForeignKey(EnvioBh, related_name='movimento', on_delete=models.CASCADE)
    tipo = models.CharField("Tipo de movimentação",choices=TIPO_CHOICE, max_length=5)
    quantidade = models.IntegerField("Quantidade", default=1)
    defeito = models.CharField("Defeito", max_length=200)

    create_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    object = models.Manager()

    
    def __str__(self):
        return str(f'{self.equipamento.name} | Defeito:  {self.defeito}')

    class Meta:
        verbose_name = "Movimento"
        verbose_name_plural = "Movimentos"