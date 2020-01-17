from django.shortcuts import render
from .forms import CeanorteForm, CEANORTE,CaixaForm

def ceanorte(request):
    template = 'ceanorte.html'
    form = CeanorteForm(request.POST or None)
    choices = CEANORTE
    context = {
        'choices' : choices,
    }
    return render(request, template,context)


def dulce(request):
    template = 'dulce.html'
    form = CaixaForm(request.POST or None)
    context = {
        'form' : form,
    }
    return render(request, template,context)
