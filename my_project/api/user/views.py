from rest_framework import viewsets
from django.http import Http404
from rest_framework.response import Response

from my_project.core.models import Profile
from .serializers import UserSerializer, UserTecnicoSerializer
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()

class UserViewset(viewsets.ModelViewSet):
    
    
    def get_serializer_class(self):
        if self.action == 'tecnicos':
            return UserTecnicoSerializer
        return UserSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        
        if self.action == 'tecnicos':
            queryset = queryset.filter(profile__cargo__in=[Profile.CARGO_GERENCIA_TI,Profile.CARGO_TECNICO])

        return queryset

    def get_object(self):
        if not self.request.user.is_authenticated:
            raise Http404

        if self.kwargs.get('pk') == 'current':
            return self.request.user

        obj = super().get_object()
       
        if not obj:
            raise Http404

        return obj

    @action(methods=['get'], detail=False)
    def tecnicos(self,request, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
