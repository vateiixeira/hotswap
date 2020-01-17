import csv 
from .models import DataInauguracao
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
        cod_filial = item.get('Cod_Filial')
        loja = str(item.get('Loja'))
        inauguracao = item.get('Inauguracao')

        """
        model = TestDataInauguracao()
        model.cod_filial = cod_filial
        model.loja = loja
        model.inauguracao = inauguracao
        print(model)"""
        
       # JOGA TUDO NUM OBJETO DE EQUIPAMENTO E ADICIONA
        lista = DataInauguracao(
            cod_filial=cod_filial,
            loja=loja, 
            inauguracao=inauguracao)
        aux.append(lista)

    
    # ADICIONA NO BANCO
    DataInauguracao.objects.bulk_create(aux)



