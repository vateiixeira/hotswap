from django.contrib import admin
from .models import *

class DataInauguracaoAdmin(admin.ModelAdmin):
    ordering = ['loja']
    search_fields = ['loja']

admin.site.register(CentralTelefonica)
admin.site.register(DataInauguracao, DataInauguracaoAdmin)


admin.site.register(CircuitoDados)
admin.site.register(CircuitoVoz)