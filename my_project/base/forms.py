from django import forms
from .models import *

class IncidenteForm(forms.ModelForm):
    class Meta:
        model = HistoricoIncidente
        fields = '__all__'        
        widgets = {
           'incidente': forms.Textarea(attrs={'cols': 60, 'rows': 8}),
           'data' : forms.TextInput(attrs={'placeholder': '16/01/2020 12:00'})
        }

class DataInauguracaoForm(forms.ModelForm):
    class Meta:
        model = DataInauguracao
        fields = '__all__'

class Circuito_VozForm(forms.ModelForm):
    class Meta:
        model = CircuitoVoz
        fields = '__all__'
        widgets = {
            'servico_equipamento' : forms.Textarea(attrs={ 'rows': 5, 'cols':30}),
        }

class CentralTelefonicaForm(forms.ModelForm):
    class Meta:
        model = CentralTelefonica
        fields = '__all__'
        widgets = {
            'obs' : forms.Textarea(attrs={ 'rows': 8, 'cols':30}),
        }
        
        