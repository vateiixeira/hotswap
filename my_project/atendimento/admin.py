from django.contrib import admin
from .models import *

class AtendimentoAdmin(admin.ModelAdmin):
    list_display = ['problema', 'setor', 'loja', 'solicitante', 'create_at']
    list_filter = ['create_at']

admin.site.register(Atendimento, AtendimentoAdmin)

