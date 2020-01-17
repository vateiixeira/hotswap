from django.shortcuts import render,redirect
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import *
from my_project.core.utils import render_to_pdf, Render
from datetime import datetime
from django.views.generic import View
from my_project.core.utils import is_staff
from django.db.models import Q
from my_project.core.models import Profile

@login_required
def cadastro(request):
    template= 'cad_transf.html' 
    form = TransferenciaForm(request.POST or None)
    if request.method =='POST':
        id_equipamento = request.POST.get('equipamento')
        cod_filial = request.POST.get('destino')
        if form.is_valid():
            # TRANSFERE FILIAL DO EQUIPAMENTO
            equip = Equipamento.object.get(id=id_equipamento)            
            filial = Lojas.object.get(id=cod_filial)
            equip.loja = filial
            equip.save()
            form.user = request.user
            form.save()
            messages.success(request, 'Transferência cadastrada com sucesso!')
            context = {'messages': messages}
            form = TransferenciaForm()
        else:
            messages.error(request, 'Formulário inválido!')
            context = {'messages': messages}
    context = {
        'staff': is_staff(request.user),
        'form': form  
    }
    return render(request,template,context)


def list_transf(request):
    template='lista_transf.html'

    grupo_usuario = Profile.objects.get(user = request.user)
    if grupo_usuario.grupo == "BH":
        transf = Transferencia.object.filter(Q(destino_id__gt = 8)).order_by('-create_at')
    elif grupo_usuario.grupo == "MONTES CLAROS":
        transf = Transferencia.object.filter(Q(destino_id__lt = 9)).order_by('-create_at')
    else:
        transf = Transferencia.object.all().order_by('-create_at')

    user = request.user
    staff = is_staff(user)
    context = {
        'staff': is_staff(request.user),
        'transf': transf,
        'staff': staff,
    }
    return render(request,template,context)
    

class UpdateTransf(UpdateView):
    template_name ='update_transf.html'
    model = Transferencia
    fields = ['equipamento', 'destino', 'obs']
    context_object_name = 'transf'

class DeleteTransf(DeleteView):
    template_name = 'delete_transf.html'
    model = Transferencia
    success_url = reverse_lazy('trans:lista_transf')

def transf_por_data_filial(request):
    template = 'viewpordatafilial_transf.html'
    dtinicial = dtfinal = 0
    if request.method == 'POST':
        form = RelatorioDataFilialForm(request.POST or None) 
        if form.is_valid():
            dtinicial = str(form.cleaned_data['inicial'])
            dtfinal = str(form.cleaned_data['final'])
            idorigem = request.POST.get('filial')       
            return redirect('transf:pdfdatafilial',dtinicial=dtinicial, dtfinal=dtfinal,idorigem=idorigem) 
        else: 
            messages.error(request, "Formulário invalido!")  
            form = RelatorioDataFilialForm() 
    else: 
        form = RelatorioDataFilialForm()
    context = {
        'staff': is_staff(request.user),
        'form': form,
    }    
    return render(request,template, context)

class PdfPorDataFilial(View):
    def get(self, request, dtinicial, dtfinal, idorigem):
        dtgeracao = datetime.now()
        origem = Lojas.object.get(id=idorigem)
        chamado = Transferencia.object.filter(create_at__lte=dtfinal, create_at__gte=dtinicial, destino=idorigem) 
        loja = Lojas.object.get(id=idorigem)
        if not chamado.exists():
            return redirect('core:erro_relatorio')
        params = {
            'staff': is_staff(request.user),
            'chamado': chamado,
            'dtgeracao': dtgeracao,
            'dtinicial': dtinicial,
            'dtfinal': dtfinal,
            'loja': loja,
            'origem': origem,
        }

        return Render.render('pdf_data_filial_transf.html', params)
