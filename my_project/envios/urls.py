from django.urls import path
from my_project.envios.views import *

app_name = 'envios'  # here for namespacing of urls.

urlpatterns = [
    path('cadastro/', envio ,name='cadastro'),
    path('listagem_envio', lista_envio, name='lista_envio'),
    path('pdf/data/<str:dtinicial>/<str:dtfinal>/', PdfPorData.as_view(), name='pdfdata'),
    path('pdf/data/recebimento/<str:dtinicial>/<str:dtfinal>/', PdfPorDataReceb.as_view(), name='pdfdata_receb'),
    path('pdf/data/<str:dtinicial>/<str:dtfinal>/<int:iddestino>/<int:idorigem>/', PdfPorDataFilial.as_view(), name='pdfdatafilial'),
    path('pdf/data/<str:dtinicial>/<str:dtfinal>/<int:usuario>', PdfPorUsuario.as_view(), name='pdfusuario'),
    path('pdf/data/recebimento/<str:dtinicial>/<str:dtfinal>/<int:usuario>', PdfPorUsuarioReceb.as_view(), name='pdfusuario_receb'),
    path('pdf/data/<str:dtinicial>/<str:dtfinal>/<str:modelo>/', PdfPorModelo.as_view(), name='pdfdatamodelo'),
    path('rel/pordata/', envio_por_data, name='envio_por_data'),
    path('rel/pordata/recebimento', recebimento_data, name='recebimento_data'),
    path('rel/pordatafilial/', envio_por_data_filial, name='envio_por_data_filial'),
    path('rel/porusuario/', envio_por_usuario, name='envio_por_usuario'),
    path('rel/porusuario/recebimento', recebimento_por_usuario, name='recebimento_por_usuario'),
    path('rel/pordatamodelo/', envio_por_modelo, name='envio_por_modelo'),
    #path('listagem/', ListaEstoque.as_view(), name='lista_chamado'),
    #path('edit/<int:pk>/', UpdateChamado.as_view(), name='update_chamado'),
    #path('delete/<int:pk>/', DeleteChamado.as_view(), name='delete_chamado'),    
]