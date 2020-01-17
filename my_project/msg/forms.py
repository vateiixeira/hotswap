from django import forms
from .models import Msg, MyModelChoiceField
from django.contrib.auth.models import User


class MsgForm(forms.ModelForm):    
    dest = MyModelChoiceField(queryset=User.objects.all().distinct())
    class Meta:
        model = Msg
        exclude = ['user', 'lida']

