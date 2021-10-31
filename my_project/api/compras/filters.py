from rest_framework import filters
from rest_framework.compat import coreapi
from my_project.core.patterns import PATTERN_DATE
from my_project.core.dates import parse_date
from datetime import timedelta


class ComprasFilterBackend(filters.BaseFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(name='loja', required=False, location='query', description='id loja'),
            coreapi.Field(name='data_de', required=False, location='query', description='data_de'),            
            coreapi.Field(name='data_ate', required=False, location='query', description='data_ate'),                      
        ]

    def filter_queryset(self, request, queryset, view):
        if request.GET.get('loja'):
            queryset = queryset.filter(filial_id=request.GET.get('loja'))
        
        data_de = request.GET.get('data_de')
        if data_de:
            if PATTERN_DATE.match(data_de):
                queryset = queryset.filter(create_at__gte=parse_date(data_de, '%Y-%m-%d'))
        
        data_ate = request.GET.get('data_ate')
        if data_ate:
            if PATTERN_DATE.match(data_ate):
                queryset = queryset.filter(create_at__lt=parse_date(data_ate, '%Y-%m-%d') + timedelta(days=1))
        
           
        return queryset