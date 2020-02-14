from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework import routers

app_name = 'api'

router = routers.DefaultRouter()
router.register('envios', Envio_List)

urlpatterns = [
    path('', include(router.urls)),
]
