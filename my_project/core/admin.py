from django.contrib import admin
from .models import *
from django.contrib.admin import AdminSite
from solo.admin import SingletonModelAdmin

AdminSite.site_header = 'Hotswap | Painel Administrativo'

@admin.register(ConfiguracaoEmail)
class ConfiguracaoEmailAdmin(SingletonModelAdmin):
   ...

@admin.register(ConfiguracaoSocin)
class ConfiguracaoSocinAdmin(SingletonModelAdmin):
   ...
@admin.register(ConfiguracaoSessoes)
class ConfiguracaoSessoesAdmin(SingletonModelAdmin):
   ...

@admin.register(NotasSocin)
class NotasSocinAdmin(admin.ModelAdmin):
   readonly_fields = ['data']
@admin.register(SessoesBlock)
class SessoesBlockAdmin(admin.ModelAdmin):
   readonly_fields = ['data']
class LojasAdmin(admin.ModelAdmin):
   list_display = ['name', 'numero', 'cnpj']
   search_fields = ['cnpj', 'numero', 'name']

admin.site.register(Lojas, LojasAdmin)
admin.site.register(Profile)
admin.site.register(Fornecedor)