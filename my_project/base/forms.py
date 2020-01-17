from django import forms
from .models import HistoricoIncidente, DataInauguracao

class IncidenteForm(forms.ModelForm):
    class Meta:
        model = HistoricoIncidente
        fields = '__all__'
        widgets = {
           'incidente': forms.Textarea(attrs={'cols': 60, 'rows': 3}),
           'data' : forms.TextInput(attrs={'placeholder': '16/01/2020 12:00'})
        }

class DataInauguracaoForm(forms.ModelForm):
    class Meta:
        model = DataInauguracao
        fields = '__all__'
        