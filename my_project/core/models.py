import os
from django.db import models
from django.contrib.auth.models import User
from django.utils.functional import cached_property
from solo.models import SingletonModel
from django.contrib.postgres.fields import ArrayField
from my_project.core.dates import normalized


GRUPO_USUARIOS_MOC = 'MONTES CLAROS'
GRUPO_USUARIOS_BH = 'BH'
GRUPO_USUARIOS_GERAL = 'GERAL'
GRUPO_USUARIOS = (
    (GRUPO_USUARIOS_MOC,"MONTES CLAROS"),
    (GRUPO_USUARIOS_BH,"BH"),
    (GRUPO_USUARIOS_GERAL,"GERAL"),
)

class Profile(models.Model):
    CARGO_TECNICO = 'tecnico'
    CARGO_GERENCIA_TI = 'gerencia_ti'
    
    CARGO_CHOICES = (
        (CARGO_GERENCIA_TI, 'Gerência TI'),
        (CARGO_TECNICO, 'Técnico'),
    )

    user = models.OneToOneField(User, related_name='profile',on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    grupo = models.CharField("Área de atuacao", max_length=20, choices=GRUPO_USUARIOS, default="BH" )
    filiais = models.ManyToManyField('core.Lojas', blank=True)
    cargo = models.CharField("Cargo", max_length=20, choices=CARGO_CHOICES, null=True,blank=True )
        
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
    polo = models.CharField("Polo", max_length=20, choices=GRUPO_USUARIOS, default="BH" )

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
    cnpj = models.CharField('CNPJ', max_length=50)
    rua = models.CharField('Rua', max_length=50)
    num_rua = models.IntegerField('Num')
    bairro = models.CharField('Bairro', max_length=50)
    cep = models.CharField('Cep',max_length=50)
    cidade = models.CharField('Cidade', max_length=50)
    garantia = models.IntegerField('Dias de garantia', default=90)

    object = models.Manager()
    
    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"
     
    def __str__(self):
        return self.name

class ConfiguracaoEmail(SingletonModel):
    telegram_notas_presas = models.BooleanField('Habilita envio de notas presas telegram', blank=True, default=True)
    send_novos_atendimentos = models.BooleanField('Envia e-mail de novos atendimentos ?', blank=True, default=True)
    send_novos_chamados = models.BooleanField('Envia e-mail de novos chamados ?', blank=True, default=True)
    
    send_notas_presas = models.BooleanField('Envia e-mail de notas presas ?', blank=True, default=True)
    notas_presas = ArrayField(models.CharField(max_length=128), default=list, blank=True)
    
    send_chamados_mensais = models.BooleanField('Envia e-mail de chamados mensais ?', blank=True, default=True)
    chamados_mensais = ArrayField(models.CharField(max_length=128), default=list, blank=True)
    
    send_atendimentos_mensais = models.BooleanField('Envia e-mail de atendimentos mensais ?', blank=True, default=True)
    atendimentos_mensais = ArrayField(models.CharField(max_length=128), default=list, blank=True)

    class Meta:
        verbose_name = 'Configuração de e-mail/Telegram'
        verbose_name_plural = 'Configurações de e-mails/Telegram'

class ConfiguracaoSocin(SingletonModel):
    user = models.CharField('Usuário do banco', blank=True, default='', max_length=128)
    password = models.CharField('Senha', blank=True, default='', max_length=128)
    database = models.CharField('Nome do banco', blank=True, default='', max_length=128)
    host = models.CharField('Host/IP do servidor', blank=True, default='', max_length=128)
    quantidade_para_ativar_envio = models.IntegerField('Quantidade de notas presas para ativar envio de e-mail', default=500)
    ultimo_envio_email_massa = models.DateTimeField('Ultimo envio em massa de e-mails alerta', null=True,blank=True)
    intervalo_entre_envios = models.IntegerField('Intervalo em minutos a considerar para reenviar e-mails em massa', default=30,blank=True)

    class Meta:
        verbose_name = 'Configuração banco Socin'
        verbose_name_plural = 'Configuração banco Socin'

class NotasSocin(models.Model):
    valor = models.IntegerField('Quantidade de notas presas', default=0)
    data = models.DateTimeField('Data', auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.valor} - {normalized(self.data)}'

    class Meta:
        verbose_name = 'Notas presas'
        verbose_name_plural = 'Notas presas'

class ConfiguracaoSessoes(SingletonModel):
    habilita_monitoramento = models.BooleanField('Habilita monitoramento no banco?', blank=True, default=True)
    habilita_telegram = models.BooleanField('Habilita envio de avisos telegram?', blank=True, default=True)
    minutos = models.IntegerField('Minutos a considerar sessao travada p/ ativar avisos', default=5 , blank=True)
    
    @cached_property
    def enabled(self):
        return self.habilita_monitoramento and self.minutos > 0

    class Meta:
        verbose_name = 'Configuração de sessoes'
        verbose_name_plural = 'Configuração de sessoes'

class SessoesBlock(models.Model):
    session_id = models.IntegerField('ID da sessao', default=0,blank=True)
    usuario = models.CharField('Usuário', blank=True, default='', max_length=128)
    terminal = models.CharField('Terminal', blank=True, default='', max_length=128)
    maquina = models.CharField('Maquina', blank=True, default='', max_length=128)
    programa = models.CharField('Programa', blank=True, default='', max_length=128)
    os_username =  models.CharField('Usuário SO', blank=True, default='', max_length=128)
    sessao_bloqueada = models.IntegerField('Sessao bloqueada', default=0,blank=True) 
    data =  models.DateTimeField('Ocorrencia', null=True,blank=True)

    class Meta:
        verbose_name = 'Sessoes bloqueadas'
        verbose_name_plural = 'Sessoes bloqueadas'

    def __str__(self) -> str:
        return f'{self.maquina} - {self.sessao_bloqueada}'