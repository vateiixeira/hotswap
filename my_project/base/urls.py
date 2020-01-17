from django.urls import path, include
from .views import *

app_name = 'base'

urlpatterns = [  
    path('CentralTelefonica/update/<int:pk>/', UpdateCentralTelefonica.as_view(), name='update_central_telefonica'),
    path('CentralTelefonica/delete/<int:pk>/', DeleteCentralTelefonica.as_view(), name='delete_central_telefonica'),  
    path('CentralTelefonica/list', list_central_telefonica, name='list_central_telefonica'),
    path('list/cirtcuitovoz', list_circuito_voz, name='list_circuito_voz'),
    path('list/cirtcuitodados', list_circuito_dados, name='list_circuito_dados'),
    path('list/inauguracao_lojas', lista_dt_inauguracao, name='lista_dt_inauguracao'),
    path('importar', importar, name='importar'),
    path('incidente/cadastro', cadastro_incidente, name='cadastro_incidente'),
    path('incidente', lista_incidente, name='lista_incidente'),
    path('incidente/edit/<int:pk>/', update_incidente, name='update_incidente'),
    path('incidente/delete/<int:pk>/', DeleteIncidente.as_view(), name='delete_incidente'),  
]