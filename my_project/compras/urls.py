from django.urls import path
from .views import *

app_name = 'compras' 

urlpatterns = [
    path('cadastro/', cadastro ,name='cadastro_compras'),
    path('edit/<int:pk>/', update_compras, name='update_compras'),
    path('delete/<int:pk>/', DeleteCompras.as_view(), name='delete_compras'), 
    path('listagem/', listagem_compras ,name='listagem_compras'),
    path('cadastro/manutencao_mensal', manutencao_mensal ,name='manutencao_mensal'),
    path('rel/manutencao_mensal', rel_manutencao_mensal ,name='rel_manutencao_mensal'),
    path('rel/vencimento/', compras_vencimento, name='compras_vencimento'),
    path('rel/completo/', compras_completo, name='compras_completo'),
    path('rel/fornecedor/', compras_fornecedor, name='compras_fornecedor'),
    path('pdf/data/total/<str:dtinicial>/<str:dtfinal>/<int:idorigem>', PdfCompletoCompras.as_view(), name='pdfcompletoacompras'),
    path('pdf/data/vencimento/<str:dtfinal>', PdfVencimentoCompras.as_view(), name='pdfcompletovencimento'),
    path('pdf/data/fornecedor/<str:dtinicial>/<str:dtfinal>/<int:fornecedor>', PdfFornecedorCompras.as_view(), name='pdffornecedorcompras'),
    path('pdf/manutencao/<str:dt_entrega>/<str:filial>', PdfManutencaoMensal.as_view(), name='pdfmanutencaomensal'),
]