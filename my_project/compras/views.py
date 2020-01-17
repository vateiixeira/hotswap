from django.shortcuts import render,redirect
from .models import *
from .forms import * 
from my_project.core.utils import is_staff
from django.views.generic import View
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from my_project.core.utils import render_to_pdf, Render
from datetime import datetime
from django.urls import reverse_lazy

def cadastro(request): 

    model = Compras()
    form = ComprasForm()

    if request.method == 'POST':
        form = ComprasForm(request.POST or None)

        if form.is_valid():

            model.num_pedido = form.cleaned_data['num_pedido']
            model.filial = form.cleaned_data['filial']
            model.fornecedor = form.cleaned_data['fornecedor']
            model.dt_vencimento = form.cleaned_data['dt_vencimento']
            model.equipamento = form.cleaned_data['equipamento']
            model.obs = form.cleaned_data['obs']
            model.user = request.user
            model.save()

            return redirect('/compras/listagem')
    else:
        form = ComprasForm()
    context = {
        'form':form
    }
    template = 'cadastro_compras.html'
    return render(request,template,context)

class DeleteCompras(DeleteView):
    template_name='delete_compras.html'
    model = Compras
    success_url = reverse_lazy('compras:listagem_compras')

def update_compras(request,pk):
    template = 'update_compras.html'
    model = Compras.objects.get(pk=pk)
    print(model.dt_vencimento)

    if request.method == 'POST':
        form = UpdateComprasForm(request.POST, instance=model)
        if form.is_valid():
            form.save()
            return redirect('compras:listagem_compras')
    else:
        form = UpdateComprasForm(instance=model)
    
    context = {
        'form':form,
        'model':model
    }
    return render(request,template,context)

def listagem_compras(request):
    
    compras = Compras.objects.all()
    user = request.user
    staff = is_staff(user)
    context = {
        'compras': compras,
        'staff': staff,
    }
    template = 'lista_compras.html'
    return render(request,template,context)

    # -----------------------------------------------------------------------------------#


def compras_completo(request):
    template = 'viewcompleto_compras.html'
    dtinicial = dtfinal = 0
    if request.method == 'POST':
        form = RelatorioCompletoForm(request.POST)
        if form.is_valid():
            dtinicial = str(form.cleaned_data['inicial'])
            dtfinal = str(form.cleaned_data['final'])
            idorigem = request.POST.get('filial')            
            return redirect('compras:pdfcompletoacompras',dtinicial=dtinicial, dtfinal=dtfinal, idorigem=idorigem) 
        else: 
            messages.error(request, "Formulário invalido!")
            form = RelatorioCompletoForm()
    else: 
        form = RelatorioCompletoForm()
    context = {
        'staff': is_staff(request.user),
        'form': form
    }    
    return render(request,template, context)


class PdfCompletoCompras(View):
    def get(self, request, dtinicial, dtfinal, idorigem):        
        titulo = 'Compras'
        dtgeracao = datetime.now()
        atendimento = Compras.objects.filter(create_at__lte=dtfinal, create_at__gte=dtinicial, filial=idorigem)
        params = {
            'atendimento': atendimento,
            'dtgeracao': dtgeracao,
            'dtinicial': dtinicial,
            'dtfinal': dtfinal,
            'titulo': titulo,
            'usuario' : request.user
        }
        return Render.render('pdf_completo_compras.html', params)    


def compras_vencimento(request):
    template = 'viewdatavencimento_compras.html'
    dtinicial = dtfinal = 0
    if request.method == 'POST':
        form = RelatorioVencimentoForm(request.POST)
        if form.is_valid():
            dtfinal = str(form.cleaned_data['final'])          
            return redirect('compras:pdfcompletovencimento',dtfinal=dtfinal) 
        else: 
            messages.error(request, "Formulário invalido!")
            form = RelatorioVencimentoForm()
    else: 
        form = RelatorioVencimentoForm()
    context = {
        'staff': is_staff(request.user),
        'form': form
    }    
    return render(request,template, context)


class PdfVencimentoCompras(View):
    def get(self, request, dtfinal):        
        titulo = 'Compras'
        dtgeracao = datetime.now()
        atendimento = Compras.objects.filter(dt_vencimento=dtfinal)
        params = {
            'atendimento': atendimento,
            'dtgeracao': dtgeracao,
            'dtfinal': dtfinal,
            'titulo': titulo,
            'usuario' : request.user
        }
        return Render.render('pdf_vencimento_compras.html', params) 


def compras_fornecedor(request):
    template = 'viewdatafornecedor_compras.html'
    dtinicial = dtfinal = 0
    if request.method == 'POST':
        form = RelatorioFornecedorForm(request.POST)
        if form.is_valid():
            dtinicial = str(form.cleaned_data['inicial'])
            dtfinal = str(form.cleaned_data['final'])
            fornecedor = request.POST.get('fornecedor')  
          
            return redirect('compras:pdffornecedorcompras',dtfinal=dtfinal,dtinicial=dtinicial,fornecedor=fornecedor) 
        else: 
            messages.error(request, "Formulário invalido!")
            form = RelatorioFornecedorForm()
    else: 
        form = RelatorioFornecedorForm()
    context = {
        'staff': is_staff(request.user),
        'form': form
    }    
    return render(request,template, context)


class PdfFornecedorCompras(View):
    def get(self, request, dtfinal,dtinicial,fornecedor):        
        titulo = 'Compras'
        dtgeracao = datetime.now()
        atendimento = Compras.objects.filter(create_at__lte=dtfinal, create_at__gte=dtinicial, fornecedor=fornecedor)
        params = {
            'atendimento': atendimento,
            'dtgeracao': dtgeracao,
            'dtinicial': dtinicial,
            'dtfinal': dtfinal,
            'titulo': titulo,
            'usuario' : request.user
        }
        return Render.render('pdf_fornecedor_compras.html', params) 