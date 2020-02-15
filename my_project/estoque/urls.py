from django.urls import path
from my_project.estoque.views import (cadastro,lista_estoque, UpdateEstoque, DeleteEstoque,ListaEstoqueQtd,
                                        importar,estoque_por_filial,estoque_por_filial,PdfPorFilial,PdfPorModelo,estoque_por_modelo,lista_backup)



app_name = 'estoque'  # here for namespacing of urls.

urlpatterns = [
    path('cadastro/', cadastro ,name='cadastro'),
    path('listagem_estoque', lista_estoque, name='lista_estoque'),
    path('listagem_estoque_qtd', ListaEstoqueQtd.as_view(), name='lista_estoque_qtd'),
    path('lista_backup', lista_backup, name='lista_backup'),
    path('edit/<int:pk>/', UpdateEstoque.as_view(), name='update_estoque'),
    path('delete/<int:pk>/', DeleteEstoque.as_view(), name='delete_estoque'),
    path('importar', importar, name='importar'),
    path('rel/porequip_filial/', estoque_por_filial, name='estoque_por_filial'),
    path('rel/por_filial/', estoque_por_filial, name='estoque_por_filial'),
    path('pdf/data/<int:idorigem>/', PdfPorFilial.as_view(), name='pdffilial'), 
    path('pdf/data/<int:idorigem>/<str:name>/', PdfPorModelo.as_view(), name='pdfmodelofilial'),
    path('rel/porfilialmodelo/', estoque_por_modelo, name='estoque_por_modelo'),
]