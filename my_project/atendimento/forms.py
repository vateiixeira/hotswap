from django import forms
from . models import Atendimento
from django.contrib.auth.models import User
from my_project.core.models import Lojas
from my_project.estoque.models import Equipamento


class AtendimentoViewForm(forms.ModelForm):
    solucao = forms.CharField(required=False, widget=forms.Textarea(attrs={'cols': 60, 'rows': 7}))
    class Meta:
        model = Atendimento
        exclude = ['user', 'user_finaliza']
        widgets = {            
            'problema': forms.Textarea(attrs={'cols': 60, 'rows': 3}),
        }


class AtendimentoForm(forms.ModelForm): 
    class Meta:
        model = Atendimento
        exclude = ("create_at", "updated_at", "user", "user_finaliza")
        widgets = {
            'problema': forms.Textarea(attrs={'rows':5, 'cols':50}),
            'solucao': forms.Textarea(attrs={'rows':5, 'cols':50}),
        }



class RelatorioTecnicoForm(forms.Form):
    inicial = forms.DateField(input_formats=['%Y-%m-%d'])
    final = forms.DateField(input_formats=['%Y-%m-%d'])
    usuario = forms.ModelChoiceField(queryset=User.objects.all())

class RelatorioCompletoTodasForm(forms.Form):
    inicial = forms.DateField(input_formats=['%Y-%m-%d'],initial= "Ano-Mês-Dia")
    final = forms.DateField(input_formats=['%Y-%m-%d'],initial= "Ano-Mês-Dia")

class RelatorioCompletoForm(forms.Form):
    inicial = forms.DateField(input_formats=['%Y-%m-%d'],initial= "Ano-Mês-Dia")
    final = forms.DateField(input_formats=['%Y-%m-%d'],initial= "Ano-Mês-Dia")
    filial = forms.ModelChoiceField(queryset=Lojas.object.all())

class RelatorioSetorForm(forms.Form):
    inicial = forms.DateField(input_formats=['%Y-%m-%d'],initial= "Ano-Mês-Dia")
    final = forms.DateField(input_formats=['%Y-%m-%d'],initial= "Ano-Mês-Dia")
    setor = forms.ChoiceField(choices=Equipamento.SETOR_CHOICES)



