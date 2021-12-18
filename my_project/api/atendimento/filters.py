from rest_framework import filters
from rest_framework.compat import coreapi
from my_project.core.patterns import PATTERN_DATE
from my_project.core.dates import parse_date
from datetime import timedelta


class AtendimentoFilterBackend(filters.BaseFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(name='loja', required=False, location='query', description='id loja'),            
            coreapi.Field(name='responsavel', required=False, location='query', description='id responsavel'),            
            coreapi.Field(name='tecnico', required=False, location='query', description='id tecnico'),            
            coreapi.Field(name='setor', required=False, location='query', description='id setor'),            
            coreapi.Field(name='data_de', required=False, location='query', description='data_de'),            
            coreapi.Field(name='data_ate', required=False, location='query', description='data_ate'),            
            coreapi.Field(name='status', required=False, location='query', description='status'),            
        ]

    def filter_queryset(self, request, queryset, view):
        if request.GET.get('loja'):
            queryset = queryset.filter(loja_id=request.GET.get('loja'))
        
        if request.GET.get('responsavel'):
            queryset = queryset.filter(responsavel_id=request.GET.get('responsavel'))
        
        if request.GET.get('tecnico'):
            queryset = queryset.filter(user_id=request.GET.get('tecnico'))
        
        if request.GET.get('setor'):
            queryset = queryset.filter(setor=request.GET.get('setor'))
        
        if request.GET.get('status'):
            queryset = queryset.filter(status=request.GET.get('status'))

        data_de = request.GET.get('data_de')
        if data_de:
            if PATTERN_DATE.match(data_de):
                queryset = queryset.filter(create_at__gte=parse_date(data_de, '%Y-%m-%d') + timedelta(days=1))
        
        data_ate = request.GET.get('data_ate')
        if data_ate:
            if PATTERN_DATE.match(data_ate):
                queryset = queryset.filter(create_at__lt=parse_date(data_ate, '%Y-%m-%d') + timedelta(days=1))
            
        return queryset