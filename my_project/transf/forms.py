from django import forms
from .models import *
from my_project.estoque.models import Equipamento
from django_select2.forms import Select2Widget
from bootstrap_datepicker_plus import DatePickerInput

class TransferenciaForm(forms.ModelForm):
    obs = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 7}))
    class Meta:
        model = Transferencia
        fields = ['equipamento', 'destino', 'obs', 'qtd']
        widgets = {
            'equipamento': Select2Widget,
            'destino': Select2Widget,
        }

class RelatorioDataFilialForm(forms.Form):
    inicial = forms.DateField(input_formats=['%Y-%m-%d'])
    final = forms.DateField(input_formats=['%Y-%m-%d'])
    filial = forms.ModelChoiceField(queryset=Lojas.object.all())