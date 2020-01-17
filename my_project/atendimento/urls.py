from django.urls import path,include
from .views import *

app_name='atendimento'

urlpatterns = [
    path('', lista_atendimento, name='lista_atendimento'),    
    path('pendente/', lista_atendimento_pendente, name='lista_atendimento_pendente'),
    path('edit/<int:pk>/', update_atendimento, name='update_atendimento'),
    path('delete/<int:pk>/', DeleteAtendimento.as_view(), name='delete_atendimento'), 
    path('rel/porusuario/', atendimento_por_tecnico, name='atendimento_por_tecnico'),
    path('rel/pordata/', atendimento_completo, name='atendimento_completo'),
    path('rel/completo/', atendimento_completo_todas, name='atendimento_completo_todas'),
    path('rel/porsetor/', atendimento_setor, name='atendimento_setor'),
    path('pdf/data/<str:dtinicial>/<str:dtfinal>/<int:usuario>', PdfTecnicoAtendimento.as_view(), name='pdftecnico'),
    path('pdf/data/total/<str:dtinicial>/<str:dtfinal>/<int:idorigem>', PdfCompletoAtendimento.as_view(), name='pdfcompletoatendimento'),
    path('pdf/data/<str:dtinicial>/<str:dtfinal>/<str:idorigem>', PdfSetorAtendimento.as_view(), name='pdfsetoratendimento'),
    path('pdf/data/<str:dtinicial>/<str:dtfinal>', PdfCompletoAtendimentoTodas.as_view(), name='pdfcompletoatendimentotodas'),
]