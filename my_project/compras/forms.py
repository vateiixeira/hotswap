from django import forms
from .models import *
from django.forms import ModelChoiceField
from django_select2.forms import Select2Widget
from datetime import date

class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return str(obj.patrimonio)


class ComprasForm(forms.ModelForm):
    num_pedido = forms.IntegerField(min_value=0, initial=0)
    dt_vencimento = forms.DateField(initial= "Ano-Mês-Dia",  input_formats=['%d-%m-%Y'])
    obs = forms.CharField(widget=forms.Textarea)
    equipamento = MyModelChoiceField(queryset=Equipamento.object.all(), widget=Select2Widget)
    class Meta:
        model = Compras
        exclude = ['create_at','updated_at','user']

class UpdateComprasForm(forms.ModelForm):
    num_pedido = forms.IntegerField(min_value=0, initial=0)
    obs = forms.CharField(widget=forms.Textarea)
    equipamento = MyModelChoiceField(queryset=Equipamento.object.all(), widget=Select2Widget)
    class Meta:
        model = Compras
        exclude = ['create_at','updated_at','user', 'dt_vencimento']

class ManutencaoMensalForm(forms.ModelForm):
    dt_ultima_manutencao = forms.DateField(initial=date.today())
    dt_aquisicao_equipamento= forms.DateField(initial=date.today())
    vencimento = forms.DateField(initial=date.today())
    class Meta:
        model = Manutencao_Mensal
        fields = '__all__'
        
class RelatorioManutencaoMensal(forms.Form):
    filial = forms.ModelChoiceField(queryset=Lojas.object.all())
    dt_entrega = forms.CharField(label='Data Entrega')

        
class RelatorioCompletoForm(forms.Form):
    inicial = forms.DateField(input_formats=['%Y-%m-%d'],initial= "Ano-Mês-Dia")
    final = forms.DateField(input_formats=['%Y-%m-%d'],initial= "Ano-Mês-Dia")
    filial = forms.ModelChoiceField(queryset=Lojas.object.all())


class RelatorioVencimentoForm(forms.Form):
    final = forms.DateField(input_formats=['%Y-%m-%d'],initial= "Ano-Mês-Dia")

class RelatorioFornecedorForm(forms.Form):
    inicial = forms.DateField(input_formats=['%Y-%m-%d'],initial= "Ano-Mês-Dia")
    final = forms.DateField(input_formats=['%Y-%m-%d'],initial= "Ano-Mês-Dia")
    fornecedor = forms.ModelChoiceField(queryset=Fornecedor.object.all())
