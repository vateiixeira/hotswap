from django.urls import path
from .views import cadastro, msg, msg_indi

app_name = 'msg' 

urlpatterns = [
    path('cadastro/', cadastro ,name='cadastro'),
    path('<int:id>/<str:grupo>', msg ,name='msg'),
    path('<int:id>', msg_indi, name='msg_indi'),

]