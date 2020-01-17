from django.urls import path,include
from .views import *

app_name = 'fc'  # here for namespacing of urls.

urlpatterns = [
    path('ceanorte/', ceanorte, name="ceanorte"),
    path('dulce/', dulce, name="dulce"),
]