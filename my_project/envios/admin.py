from django.contrib import admin
from .models import EnvioBh,Recebimento


class EnvioAdmin(admin.ModelAdmin):
    # CRIA DISPLAY DE VISUALIZACAO DOS CAMPOS EXISTENTES NESSA TABELA
    list_display = ['filial_origem', 'filial_destino', 'create_at', 'user']
    list_filter = ['create_at']

admin.site.register(EnvioBh, EnvioAdmin)
admin.site.register(Recebimento)
