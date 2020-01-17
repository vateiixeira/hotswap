import csv 
from .models import *
from my_project.core.models import Lojas
import os
import sys
import codecs


def csv_to_list(filename):  
    f=codecs.open(filename,"rt")
    csvread=csv.DictReader(f,delimiter=',')
    csv_data = [line for line in csvread]
    aux = []

    for item in csv_data:
        regiao_filial = item.get('Filial')
        operadora = item.get('Operadora')
        designacao = item.get('Designacao')
        servico_equipamento = item.get('Servico')
        tel_abrir_chamado = item.get('Abertura')
        op_urla = item.get('Urla')    
        
       # JOGA TUDO NUM OBJETO DE EQUIPAMENTO E ADICIONA
        lista = CircuitoVoz(
            regiao_filial = regiao_filial,
            operadora = operadora,
            designacao = designacao,
            servico_equipamento = servico_equipamento,
            tel_abrir_chamado = tel_abrir_chamado,
            op_urla = op_urla
        )
        aux.append(lista)

    
    # ADICIONA NO BANCO
    CircuitoVoz.objects.bulk_create(aux)



