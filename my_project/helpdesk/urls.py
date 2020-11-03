from django.urls import path,include
from .views import *


app_name = 'helpdesk'  # here for namespacing of urls.

urlpatterns = [
    path('', help_desk, name='help_desk'),
]