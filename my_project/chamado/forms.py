from django import forms
from django.forms import ModelChoiceField
from my_project.estoque.models import Equipamento
from my_project.core.models import Lojas
from django_select2.forms import Select2Widget
from django.contrib.auth.models import User
from .models import Chamado

    
SIT_CHOICE = [
    ("p", "PENDENTE"),
    ("r", "RESOLVIDO"),
    ("c", "COMPRADO"),
    ("o", "RECOLHIDO"),
]

class UpdateChamadoForm(forms.ModelForm):
    defeito = forms.CharField(widget=forms.TextInput(attrs={'size':'60'}))
    quantidade = forms.IntegerField(min_value=0, widget=forms.TextInput(attrs={'size':'8'}))
    valor = forms.DecimalField(min_value=0, decimal_places=2, widget=forms.TextInput(attrs={'size':'8'}))
    dt_finalizado = forms.DateField(input_formats=['%Y-%m-%d'],initial= "Ano-Mês-Dia")
    class Meta:
        model = Chamado
        fields = ['chamado','modelo','serial','loja','defeito','quantidade','valor','status','dt_finalizado']


class ChamadoForm(forms.Form):
    chamado = forms.IntegerField()    
    modelo = forms.ModelChoiceField(queryset=Equipamento.object.all().values_list('modelo', flat=True).distinct(), 
    to_field_name='modelo',widget=Select2Widget)
    serial = forms.ModelChoiceField(queryset=Equipamento.object.all().values_list('serial', flat=True).distinct(), 
    to_field_name='serial',widget=Select2Widget)
    loja = forms.ModelChoiceField(queryset=Lojas.object.all())
    defeito = forms.CharField(widget=forms.Textarea)
    valor = forms.DecimalField(max_digits=7, decimal_places=2)
    status = forms.ChoiceField(choices=SIT_CHOICE)

class RelatorioDataForm(forms.Form):
    inicial = forms.DateField(input_formats=['%Y-%m-%d'],initial= "Ano-Mês-Dia")
    final = forms.DateField(input_formats=['%Y-%m-%d'],initial= "Ano-Mês-Dia")

class RelatorioDataFilialForm(forms.Form):
    inicial = forms.DateField(input_formats=['%Y-%m-%d'],initial= "Ano-Mês-Dia")
    final = forms.DateField(input_formats=['%Y-%m-%d'],initial= "Ano-Mês-Dia")
    filial = forms.ModelChoiceField(queryset=Lojas.object.all())

class RelatorioUsuarioForm(forms.Form):
    inicial = forms.DateField(input_formats=['%Y-%m-%d'])
    final = forms.DateField(input_formats=['%Y-%m-%d'])
    usuario = forms.ModelChoiceField(queryset=User.objects.all())


    