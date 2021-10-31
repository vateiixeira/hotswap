from rest_framework import filters
from rest_framework.compat import coreapi


class EquipamentoFilterBackend(filters.BaseFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(name='loja', required=False, location='query', description='loja'),            
            coreapi.Field(name='setor', required=False, location='query', description='setor'),            
            coreapi.Field(name='backup', required=False, location='query', description='backup'),            
        ]

    def filter_queryset(self, request, queryset, view):
        if request.GET.get('loja'):
            queryset = queryset.filter(loja_id=request.GET.get('loja'))
        
        if request.GET.get('setor'):
            queryset = queryset.filter(setor=request.GET.get('setor'))
        
        if request.GET.get('backup'):
            backup = True if request.GET.get('backup') == 'true' else False
            queryset = queryset.filter(backup=backup)

        return queryset