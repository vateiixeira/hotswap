from django.contrib import admin
from .models import *
from django.contrib.admin import AdminSite

AdminSite.site_header = 'Hotswap | Painel Administrativo'

class LojasAdmin(admin.ModelAdmin):
   list_display = ['name', 'numero', 'cnpj']
   search_fields = ['cnpj', 'numero', 'name']

admin.site.register(Lojas, LojasAdmin)
admin.site.register(Profile)
admin.site.register(Fornecedor)