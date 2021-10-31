from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('my_project.core.urls')),
    path("estoque/", include('my_project.estoque.urls')),
    path("chamado/", include('my_project.chamado.urls')),    
    path("envio/", include('my_project.envios.urls')),   
    path("transf/", include('my_project.transf.urls')),   
    path("frentecaixa/", include('my_project.frentecaixa.urls')),  
    path("msg/", include('my_project.msg.urls')),  
    path('admin/', admin.site.urls),
    path("atendimento/", include('my_project.atendimento.urls')),   
    path("compras/", include('my_project.compras.urls')),   
    path("base/", include('my_project.base.urls')),   
    path("api/", include('my_project.api.urls')),   
    path("helpdesk/", include('my_project.helpdesk.urls')),     
]
