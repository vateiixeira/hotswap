from my_project.core.models import Lojas
import csv
import os
import sys
import codecs

filename = os.path.join(os.path.dirname(os.path.dirname(__file__)),'filial.csv')

def csv_to_list(filename):  
    # MUDA PARA UTF16 PORQUE SE TIVER ALGUM BYTE NULOE ELE NAO IMPORTA
    f=codecs.open(filename,"rb","utf-16")
    csvread=csv.DictReader(f,delimiter=',')
    csv_data = [line for line in csvread]

    aux = []

    for item in csv_data:
        name = item.get('NAME')
        numero = str(item.get('CODIGO'))
        cnpj = item.get('CGC')
        rua = item.get('ENDERECO')
        num_rua = item.get('NUMERO')
        bairro = item.get('BAIRRO')
        cep = item.get('CEP')
        cidade = item.get('CIDADE')

        #JOGA TUDO NUM OBJETO DE EQUIPAMENTO E ADICIONA
        lista = Lojas(
            name=name,
            numero=numero, 
            cnpj=cnpj, 
            rua=rua, 
            num_rua=num_rua, 
            bairro=bairro,
            cep=cep, 
            cidade=cidade)
        aux.append(lista)    
    # ADICIONA NO BANCO
    Lojas.object.bulk_create(aux)



