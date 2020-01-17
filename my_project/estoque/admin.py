from django.contrib import admin
from .models import Equipamento,Movimento

class EquipamentoAdmin(admin.ModelAdmin):
    list_display=['modelo', 'name','serial','patrimonio']
    search_fields=['name','modelo','serial','patrimonio']
    empty_value_display = '-empty-'

class MovimentoAdmin(admin.ModelAdmin):
    list_display=['equipamento', 'envio', 'defeito', 'tipo']
    list_filter= ['create_at']


admin.site.register(Equipamento, EquipamentoAdmin)
admin.site.register(Movimento,MovimentoAdmin)