from django.urls import path
from .views import list_transf,UpdateTransf,DeleteTransf,cadastro,PdfPorDataFilial,transf_por_data_filial

app_name = 'transf' 

urlpatterns = [
    path('cadastro/', cadastro ,name='cadastro'),
    path('listagem_transf', list_transf, name='lista_transf'),
    path('edit/<int:pk>/', UpdateTransf.as_view(), name='update_transf'),
    path('delete/<int:pk>/', DeleteTransf.as_view(), name='delete_transf'),
    path('pdf/data/<str:dtinicial>/<str:dtfinal>/<int:idorigem>/', PdfPorDataFilial.as_view(), name='pdfdatafilial'), 
    path('rel/pordatafilial/', transf_por_data_filial, name='transf_por_data_filial'),
]