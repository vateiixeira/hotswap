from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, viewsets
from django.contrib.auth.models import User
from django.middleware.csrf import get_token
from my_project.envios.models import EnvioBh
from .serializers import Envio_Serializer

class Envio_List(viewsets.ModelViewSet):
    queryset = EnvioBh.object.all()
    serializer_class = Envio_Serializer

