from django.contrib import admin
from django.urls import path, include
from my_project.api.base.views import CentralTelefonicaViewset, CircuitoDadosViewset, CircuitoVozViewset, DataInauguracaoViewset, FeriasViewset, HistoricoIncidenteViewset, IpFixoViewset

from my_project.api.compras.views import ComprasViewset
from my_project.core.views import notas_travadas_mysql
from .views import *
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token
from .user.views import UserViewset
from .equipamento.views import EquipamentoViewset,CategoriaHDViewset,CategoriaMemoriaViewset,CategoriaProcessadorViewset,CategoriaSOViewset
from .core.views import DashboardView, FornecedorViewset, LojasViewset
from .chamado.views import lista_status_chamados,ChamadoViewset
from .estoque.views import EnvioViewset
from .transf.views import TransferenciaViewset
from .atendimento.views import AtendimentoViewset


app_name = 'api'

router = routers.DefaultRouter()
router.register('envios', Envio_List)
router.register('users', UserViewset, basename='users')


router.register('equipamento', EquipamentoViewset, basename='equipamento')
router.register('categoria-hd', CategoriaHDViewset, basename='hd')
router.register('categoria-memoria', CategoriaMemoriaViewset, basename='memoria')
router.register('categoria-processador', CategoriaProcessadorViewset, basename='processador')
router.register('categoria-so', CategoriaSOViewset, basename='so')
router.register('lojas', LojasViewset, basename='lojas')
router.register('fornecedor', FornecedorViewset, basename='fornecedor')
router.register('chamado', ChamadoViewset, basename='chamado')
router.register('envio', EnvioViewset, basename='envio')
router.register('transferencia', TransferenciaViewset, basename='transferencia')
router.register('atendimento', AtendimentoViewset, basename='atendimento')
router.register('compras', ComprasViewset, basename='compras')
router.register('base-conhecimento/circuito-voz', CircuitoVozViewset, basename='circuito-voz')
router.register('base-conhecimento/circuito-dados', CircuitoDadosViewset, basename='circuito-dados')
router.register('base-conhecimento/inauguracoes', DataInauguracaoViewset, basename='inauguracoes')
router.register('base-conhecimento/centrais-telefonicas', CentralTelefonicaViewset, basename='centrais-telefonicas')
router.register('base-conhecimento/historico-incidente', HistoricoIncidenteViewset, basename='historico-incidente')
router.register('base-conhecimento/ips-camara-fria', IpFixoViewset, basename='ips-camara-fria')
router.register('base-conhecimento/ferias', FeriasViewset, basename='ferias')
#router.register('dashboard', DashboardView, basename='dashboard')

urlpatterns = [
    path('', include(router.urls)),
    path('helpdesk/usuario/<int:id>', user_helpdesk),
    path('helpdesk/novo/atendimento', novo_atendimento_helpdesk),
    path('helpdesk/lista', list_atendimento_helpdesk),
    path('change_date', change_date, name='change_date'),
    path('login/', obtain_jwt_token, name='login'),
    path('refresh-token', change_date, name='change_date'),
    path('setores/', lista_setores, name='setores'),
    path('polos/', lista_polos, name='setores'),
    path('lista-status-chamado/', lista_status_chamados, name='lista-status-chamado'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('ajax/notas_travadas_mysql/', notas_travadas_mysql, name='notas_travadas_mysql'),

]
