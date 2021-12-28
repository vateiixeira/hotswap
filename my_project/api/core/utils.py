

from my_project.atendimento.models import Atendimento
from my_project.chamado.models import Chamado
from my_project.core.views import get_data_final_mes
from django.utils import timezone


def get_data_year_chamado(filiais):
    ano = timezone.now().year
    janeiro = Chamado.object.filter(create_at__lte=f'{ano}-1-31', create_at__gte=f'{ano}-1-1', loja__in = filiais).count()
    fevereiro = Chamado.object.filter(create_at__lte=f'{ano}-2-28', create_at__gte=f'{ano}-2-1', loja__in = filiais).count()
    marco = Chamado.object.filter(create_at__lte=f'{ano}-3-31', create_at__gte=f'{ano}-3-1', loja__in = filiais).count()
    abril = Chamado.object.filter(create_at__lte=f'{ano}-4-30', create_at__gte=f'{ano}-4-1', loja__in = filiais).count()
    maio = Chamado.object.filter(create_at__lte=f'{ano}-5-31', create_at__gte=f'{ano}-5-1', loja__in = filiais).count()
    jun = Chamado.object.filter(create_at__lte=f'{ano}-6-30', create_at__gte=f'{ano}-6-1', loja__in = filiais).count()
    julho = Chamado.object.filter(create_at__lte=f'{ano}-7-31', create_at__gte=f'{ano}-7-1', loja__in = filiais).count()
    agosto = Chamado.object.filter(create_at__lte=f'{ano}-8-31', create_at__gte=f'{ano}-8-1', loja__in = filiais).count()
    setembro = Chamado.object.filter(create_at__lte=f'{ano}-9-30', create_at__gte=f'{ano}-9-1', loja__in = filiais).count()
    outubro = Chamado.object.filter(create_at__lte=f'{ano}-10-31', create_at__gte=f'{ano}-10-1', loja__in = filiais).count()
    novembro = Chamado.object.filter(create_at__lte=f'{ano}-11-30', create_at__gte=f'{ano}-11-1', loja__in = filiais).count()
    dezembro = Chamado.object.filter(create_at__lte=f'{ano}-12-31', create_at__gte=f'{ano}-12-1', loja__in = filiais).count()
    return [janeiro , fevereiro, marco, abril, maio, jun, julho, agosto, setembro, outubro,novembro,dezembro]

def get_data_year_atendimento(filiais):
    ano = timezone.now().year
    janeiro = Atendimento.object.filter(create_at__lte=f'{ano}-1-31', create_at__gte=f'{ano}-1-1', loja__in = filiais).count()
    fevereiro = Atendimento.object.filter(create_at__lte=f'{ano}-2-28', create_at__gte=f'{ano}-2-1', loja__in = filiais).count()
    marco = Atendimento.object.filter(create_at__lte=f'{ano}-3-31', create_at__gte=f'{ano}-3-1', loja__in = filiais).count()
    abril = Atendimento.object.filter(create_at__lte=f'{ano}-4-30', create_at__gte=f'{ano}-4-1', loja__in = filiais).count()
    maio = Atendimento.object.filter(create_at__lte=f'{ano}-5-31', create_at__gte=f'{ano}-5-1', loja__in = filiais).count()
    jun = Atendimento.object.filter(create_at__lte=f'{ano}-6-30', create_at__gte=f'{ano}-6-1', loja__in = filiais).count()
    julho = Atendimento.object.filter(create_at__lte=f'{ano}-7-31', create_at__gte=f'{ano}-7-1', loja__in = filiais).count()
    agosto = Atendimento.object.filter(create_at__lte=f'{ano}-8-31', create_at__gte=f'{ano}-8-1', loja__in = filiais).count()
    setembro = Atendimento.object.filter(create_at__lte=f'{ano}-9-30', create_at__gte=f'{ano}-9-1', loja__in = filiais).count()
    outubro = Atendimento.object.filter(create_at__lte=f'{ano}-10-31', create_at__gte=f'{ano}-10-1', loja__in = filiais).count()
    novembro = Atendimento.object.filter(create_at__lte=f'{ano}-11-30', create_at__gte=f'{ano}-11-1', loja__in = filiais).count()
    dezembro = Atendimento.object.filter(create_at__lte=f'{ano}-12-31', create_at__gte=f'{ano}-12-1', loja__in = filiais).count()
    return [janeiro , fevereiro, marco, abril, maio, jun, julho, agosto, setembro, outubro,novembro,dezembro]