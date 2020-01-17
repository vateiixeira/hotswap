from django.urls import path,include
from my_project.core.views import *




app_name = 'core'  # here for namespacing of urls.

urlpatterns = [
    path('', homepage, name="homepage"),
    path('register/', register, name='register'),
    path('change_password', change_password, name='change_password'),
    path("logout/", logout_request, name="logout"),
    path("login/", login_request, name='login'),
    path('cad_fornecedor', fornecedores, name='fornecedores' ),  
    path('cad_loja', loja, name='cad_loja' ),  
    path('sessao_oracle', sessao_oracle, name='sessao_oracle' ),  
    path('erro_relatorio', erro_relatorio, name='erro_relatorio' ),  
    path('ajax/validate_username/',validate_username, name='validate_username'),
    path('ajax/get_modelo/', get_modelo, name='get_modelo'),
    path('ajax/notas_travadas_mysql/', notas_travadas_mysql, name='notas_travadas_mysql'),
    path('ajax/sessao_travada/', sessao_travada, name='sessao_travada'),
    path('import/', sessao_travada, name='sessao_travada'),
]