import csv 
from .models import Equipamento
from my_project.core.models import Lojas
import os
import sys
import codecs

filename = os.path.join(os.path.dirname(os.path.dirname(__file__)),'equip_moc.csv')

def csv_to_list(filename):  
    # MUDA PARA UTF16 PORQUE SE TIVER ALGUM BYTE NULOE ELE NAO IMPORTA
    f=codecs.open(filename,"rt")
    csvread=csv.DictReader(f,delimiter=',')
    csv_data = [line for line in csvread]

    aux = []

    for item in csv_data:
        nome = item.get('nome')
        modelo = str(item.get('modelo'))
        status = item.get('status')
        serie = item.get('serie')
        patrimonio = item.get('patrimonio')
        filial = item.get('filial')
        setor = item.get('setor')
        obs = item.get('obs')
        pk = item.get('pk')
        
        if status == 'TRUE':
            status = True
        elif status == 'FALSE':
            status = False

        #JOGA TUDO NUM OBJETO DE EQUIPAMENTO E ADICIONA
        lista = Equipamento(pk=pk,
                name=nome, 
                modelo=modelo, 
                serial=serie, 
                patrimonio=patrimonio, 
                backup=status,
                setor=setor, 
                loja=Lojas.object.get(numero=filial), 
                obs=obs)
        aux.append(lista)   
    # ADICIONA NO BANCO
    Equipamento.object.bulk_create(aux)



