from django import forms
from .models import *
from django.contrib.auth.models import User




class LojasForm(forms.ModelForm):
    cep = forms.CharField(widget=forms.TextInput(attrs={'data-mask':"00.000-000"}))
    cnpj = forms.CharField(widget=forms.TextInput(attrs={'data-mask':"00.000/0000-00"}))
    class Meta:
        model = Lojas
        fields = ['name','numero','cnpj','rua','num_rua','bairro','cep']


class CriarUsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['grupo']


class FornecedoresForm(forms.ModelForm):
    name = forms.CharField(label='Nome',widget=forms.TextInput(attrs={'size':'60'}))
    numero = forms.IntegerField(min_value=0,label='Número', widget=forms.TextInput(attrs={'size':'3'}))
    num_rua = forms.IntegerField(min_value=0, label='Número', widget=forms.TextInput(attrs={'size':'3'}))
    razao_social = forms.CharField(widget=forms.TextInput(attrs={'size':'40'}))
    rua = forms.CharField(widget=forms.TextInput(attrs={'size':'40'}))
    bairro = forms.CharField(widget=forms.TextInput(attrs={'size':'40'}))
    cep = forms.CharField(widget=forms.TextInput(attrs={'data-mask':"00.000-000"}))
    cnpj = forms.CharField(widget=forms.TextInput(attrs={'data-mask':"00.000.000/0000-00"}))

    class Meta:
        model = Fornecedor
        fields = '__all__'