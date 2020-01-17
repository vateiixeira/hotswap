from django.db import models
from django.contrib.auth.models import User

GRUPO_USUARIOS = (
    ("MONTES CLAROS","MONTES CLAROS"),
    ("BH","BH"),
    ("GERAL","GERAL"),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    grupo = models.CharField("Area de atuacao", max_length=20, choices=GRUPO_USUARIOS, default="BH" )
        
    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
     
    def __str__(self):
        return str(self.user)

class Lojas(models.Model):
    name = models.CharField('Nome', max_length=50)
    numero = models.IntegerField('Número')
    cnpj = models.CharField('CNPJ',max_length=20)
    rua = models.CharField('Rua', max_length=50)
    num_rua = models.IntegerField('Num')
    bairro = models.CharField('Bairro', max_length=50)
    cep = models.CharField('cep',max_length=20)
    cidade = models.CharField('Cidade', max_length=50)

    object = models.Manager()
    
    class Meta:
        verbose_name = "Loja"
        verbose_name_plural = "Lojas"
     
    def __str__(self):
        return self.name


class Fornecedor(models.Model):
    name = models.CharField('Nome', max_length=50)
    numero = models.IntegerField('Número da unidade', blank=True, null=True)
    razao_social = models.CharField('Razão Social', max_length=70)
    cnpj = models.IntegerField('CNPJ')
    rua = models.CharField('Rua', max_length=50)
    num_rua = models.IntegerField('Num')
    bairro = models.CharField('Bairro', max_length=50)
    cep = models.IntegerField('cep')
    cidade = models.CharField('Cidade', max_length=50)

    object = models.Manager()
    
    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"
     
    def __str__(self):
        return self.name

