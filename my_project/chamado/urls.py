from django.urls import path
from my_project.chamado.views import *


app_name = 'chamado'  # here for namespacing of urls.

urlpatterns = [
    path('cadastro/', cadastro ,name='cadastro'),
    path('listagem/', lista_chamado, name='lista_chamado'),
    path('listagem/pendente', lista_chamado_pendente, name='lista_chamado_pendente'),
    path('edit/<int:pk>/', update_chamado, name='update_chamado'),
    path('delete/<int:pk>/', DeleteChamado.as_view(), name='delete_chamado'),  
    path('rel/pordata/', chamado_por_data, name='chamado_por_data'),
    path('pdf/data/<str:dtinicial>/<str:dtfinal>/', PdfPorData.as_view(), name='pdfdata'), 
    path('pdf/data/<str:dtinicial>/<str:dtfinal>/<int:idorigem>/', PdfPorDataFilial.as_view(), name='pdfdatafilial'), 
    path('rel/pordatafilial/', chamado_por_data_filial, name='chamado_por_data_filial'),
    path('rel/porusuario/', chamado_por_usuario, name='chamado_por_usuario'),
    path('pdf/data/<str:dtinicial>/<str:dtfinal>/<int:usuario>', PdfPorUsuario.as_view(), name='pdfusuario'),
    path('change_date', change_date, name='change_date'),
]