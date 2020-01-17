from django import forms
from .models import *
from my_project.estoque.models import Equipamento, Movimento
from django_select2.forms import Select2Widget

class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamento
        fields = ['name', 'modelo','serial','patrimonio','backup','setor','loja']


class MovimentoForm(forms.ModelForm):
    class Meta:
        model = Movimento
        exclude = ['envio']
        widgets = {
            'equipamento': Select2Widget
        }

class ViewFilialForm(forms.Form):
    filial = forms.ModelChoiceField(queryset=Lojas.object.all())

class ViewModeloForm(forms.Form):
    filial = forms.ModelChoiceField(queryset=Lojas.object.all())
    modelo = forms.ModelChoiceField(queryset=Equipamento.object.all().values_list('modelo', flat=True).distinct(), 
    to_field_name='modelo',widget=Select2Widget)