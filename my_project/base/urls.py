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
    path('camara_fria/', camara_fria, name='camara_fria'),  
    path('ferias/', ferias, name='ferias'),  
    path('ferias/update/<int:pk>/', UpdateFerias.as_view(), name='update_ferias'),
    path('ferias/delete/<int:pk>/', DeleteFerias.as_view(), name='delete_ferias'),
    path('camara/update/<int:pk>/', UpdateCamara_Fria.as_view(), name='update_camara_fria'),
    path('camara/delete/<int:pk>/', DeleteCamara_Fria.as_view(), name='delete_camara_fria'),
    path('circuitovoz/update/<int:pk>/', Update_Circuito_Voz.as_view(), name='update_circuito_voz'),
    path('circuitovoz/delete/<int:pk>/', Delete_Circuito_Voz.as_view(), name='delete_circuito_voz'),
    path('circuitodados/update/<int:pk>/', Update_Circuito_Dados.as_view(), name='update_circuito_dados'),
    path('circuitodados/delete/<int:pk>/', Delete_Circuito_Dados.as_view(), name='delete_circuito_dados'),
]