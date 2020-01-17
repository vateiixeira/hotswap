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
        nome_filial = item.get('NOME')
        cod_filial = item.get('FILIAL')
        faixa_ip = item.get('FAIXA IP')
        produto = item.get('PRODUTO')
        circuito = item.get('CIRCUITO')
        roteador = item.get('ROTEADOR')    
        velocidade = item.get('VELOC')   
        
       # JOGA TUDO NUM OBJETO DE EQUIPAMENTO E ADICIONA
        lista = CircuitoDados(
            nome_filial = nome_filial,
            cod_filial = cod_filial,
            faixa_ip = faixa_ip,
            produto = produto,
            circuito = circuito,
            roteador = roteador,
            velocidade = velocidade,
        )
        aux.append(lista)

    
    # ADICIONA NO BANCO
    CircuitoDados.objects.bulk_create(aux)



