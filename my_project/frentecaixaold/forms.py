from django import forms
from my_project.estoque.models import Equipamento


CEANORTE= (
    ("PEDRO"),
    ("RAISSA"),
    ("JOSUÉ"),
    )

class CeanorteForm(forms.Form):
    pessoa = forms.ChoiceField(choices=CEANORTE, required=True, label="", initial='', widget=forms.Select())