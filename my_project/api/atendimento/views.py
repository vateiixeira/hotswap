from rest_framework.decorators import api_view
from rest_framework.response import Response
from my_project.api.atendimento.filters import AtendimentoFilterBackend
from my_project.atendimento.models import Atendimento
from rest_framework import viewsets
from django.http import Http404
from .serializers import *


class AtendimentoViewset(viewsets.ModelViewSet):
    filter_backends = [AtendimentoFilterBackend]

    def get_serializer_class(self):
        if self.action in ['list','retrieve']:
            return AtendimentoListSerializer
        return AtendimentoSerializer

    def get_queryset(self):
        queryset = Atendimento.object.all().order_by('-id')

        queryset = queryset.filter(loja__in=self.request.user.profile.filiais.all())

        return queryset

    def partial_update(self, request, *args, **kwargs):
        super().partial_update(request, *args, **kwargs)
        obj = self.get_object()
        serializer = AtendimentoListSerializer(obj)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        obj = self.get_object()
        serializer = AtendimentoListSerializer(obj)
        return Response(serializer.data)