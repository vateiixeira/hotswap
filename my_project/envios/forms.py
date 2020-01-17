from django import forms
from .models import *
from django.forms import ModelChoiceField
from my_project.estoque.models import Equipamento
from my_project.core.models import Lojas
import datetime
from django_select2.forms import Select2Widget

class EnvioForm(forms.ModelForm):
    class Meta:
        model = EnvioBh
        fields = ['filial_origem', 'filial_destino', 'num_nota', 'num_ficha_transf']
        

class RelatorioDataForm(forms.Form):
    inicial = forms.DateField(input_formats=['%Y-%m-%d'],initial= "Ano-Mês-Dia")
    final = forms.DateField(input_formats=['%Y-%m-%d'],initial= "Ano-Mês-Dia")

class RelatorioDataFilialForm(forms.Form):
    inicial = forms.DateField(input_formats=['%Y-%m-%d'],initial= "Ano-Mês-Dia")
    final = forms.DateField(input_formats=['%Y-%m-%d'],initial= "Ano-Mês-Dia")
    filial_origem = forms.ModelChoiceField(queryset=Lojas.object.all())
    filial_destino = forms.ModelChoiceField(queryset=Lojas.object.all())

class RelatorioUsuarioForm(forms.Form):
    inicial = forms.DateField(input_formats=['%Y-%m-%d'],initial= "Ano-Mês-Dia")
    final = forms.DateField(input_formats=['%Y-%m-%d'],initial= "Ano-Mês-Dia")
    usuario = forms.ModelChoiceField(queryset=User.objects.all())

class RelatorioDataModeloForm(forms.Form):
    inicial = forms.DateField(input_formats=['%Y-%m-%d'],initial= "Ano-Mês-Dia")
    final = forms.DateField(input_formats=['%Y-%m-%d'],initial= "Ano-Mês-Dia")
    modelo = forms.ModelChoiceField(queryset=Equipamento.object.all().values_list('name', flat=True).distinct(), 
    to_field_name='name',widget=Select2Widget)