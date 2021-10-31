from django import forms
from django.forms import ModelChoiceField
from my_project.estoque.models import Equipamento
from my_project.core.models import Fornecedor, Lojas
from django_select2.forms import Select2Widget
from django.contrib.auth.models import User
from .models import Chamado
from bootstrap_datepicker_plus import DatePickerInput


class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return str(obj.modelo)
    

class UpdateChamadoForm(forms.ModelForm):
    #defeito = forms.CharField(widget=forms.TextInput(attrs={'size':'60'}))
    quantidade = forms.IntegerField(min_value=0, widget=forms.TextInput(attrs={'size':'8'}))
    valor = forms.DecimalField(min_value=0, decimal_places=2, widget=forms.TextInput(attrs={'size':'8'}))
    dt_finalizado = forms.DateField(label='Data de finalização',widget=DatePickerInput(format='%d/%m/%Y',
                        options={
                            'locale': 'pt-br'
                        }),required=False)
    #create_at = forms.DateField(input_formats=['%d-%m-%Y'],label='Data de finalização',widget=DatePickerInput(attrs={'type':'date'}),required=False,disabled=True)

    def clean(self):
        form_data = self.cleaned_data
        status = self.cleaned_data.get('status')
        if form_data.get('dt_finalizado',None):
            if status == Chamado.STATUS_CHAMADO_PENDENTE:
                self._errors["dt_finalizado"] = ["Quando é preenchido a data de finalização, deve-se escolher um status diferente de pendente."]
        return form_data
    class Meta:
        model = Chamado
        fields = ['chamado','modelo','serial','loja','defeito','quantidade','valor','status','dt_finalizado', 'fornecedor', 'justificativa']


class ChamadoForm(forms.Form):
    fornecedor = forms.ModelChoiceField(queryset=Fornecedor.object.all())
    chamado = forms.IntegerField()    
    modelo = forms.ModelChoiceField(queryset=Equipamento.object.all().values_list('modelo', flat=True).distinct(),widget=Select2Widget)
    serial = forms.ModelChoiceField(queryset=Equipamento.object.all().values_list('serial', flat=True).distinct(),widget=Select2Widget)
    loja = forms.ModelChoiceField(queryset=Lojas.object.all())
    defeito = forms.CharField(widget=forms.Textarea)
    valor = forms.DecimalField(max_digits=7, decimal_places=2,widget=forms.TextInput(attrs={'placeholder': '000.00'}))
    status = forms.ChoiceField(choices=Chamado.STATUS_CHAMADO_CHOICES)
    justificativa = forms.CharField(widget=forms.Textarea, required=False)
    nfe = forms.CharField(label='NF-e',widget=forms.TextInput(attrs={'placeholder': 'Número da nota fiscal'}), required=False)

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


    