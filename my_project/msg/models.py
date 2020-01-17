from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelChoiceField

#RETORNA O FIRST_NAME PARA QUE VALIDE O FORM. ISSO SUBSTITIU O VALUE_LIST 
class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.first_name

GRUPOMSG = [
    ('admin', 'Administradores'),
    ('sup', 'Supervisores'),
    ('tec', 'Técnicos'),
    ('membro', 'Membros'),
]


GRUPOIMPORTANCIA = [
    ('baixa', 'Baixa'),
    ('media', 'Média'),
    ('alta', 'Alta'),
]

class Msg(models.Model):    
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    dest = models.ForeignKey(User, related_name="destinatario", on_delete=models.CASCADE)
    assunto = models.CharField("Assunto", max_length=50)
    mensagem = models.TextField("Mensagem")
    grupo = models.CharField("Grupo", choices=GRUPOMSG, max_length=20)
    importancia = models.CharField("Importância", choices=GRUPOIMPORTANCIA, max_length=50, default='baixa')
    geral = models.BooleanField("Enviar para todos do grupo", default=False) # FALSE = NAO ENVIA PARA TODOS
    lida = models.BooleanField("Mensagme lida/não.", default=False) #FALSE = NÃO LIDA.


    create_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)    

    
    object = models.Manager()

    def __str__(self):
        return self.assunto

    class Meta:
        verbose_name = "Mensagem"
        verbose_name_plural = "Mensagens"
        

class Group_Msg(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    grupo = models.CharField("Grupo", choices=GRUPOMSG, max_length=20)

    object = models.Manager()

    def __str__(self):
        return self.grupo

    class Meta:
        verbose_name = "Grupo"
        verbose_name_plural = "Grupos"




