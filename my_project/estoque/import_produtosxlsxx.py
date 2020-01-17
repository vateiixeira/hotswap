import xlrd 
from .models import Equipamento
from my_project.core.models import Lojas
import os

def xlsx():
    filename = os.path.join(os.path.dirname(os.path.dirname(__file__)),'1.xlsx')

    worbook = xlrd.open_workbook(filename)
    sheet = worbook.sheet_by_index(0)


    fields = ('Nome', 'Modelo', 'Serie', 'Patrimonio', 'Status','Setor', 'Filial', 'Obs')

    aux = []

    for row in range(1, sheet.nrows):
        nome = sheet.row(row)[0].value
        modelo = sheet.row(row)[1].value
        serie = sheet.row(row)[2].value
        patrimonio = sheet.row(row)[3].value
        status = sheet.row(row)[4].value
        setor = sheet.row(row)[5].value
        filial = sheet.row(row)[6].value
        obs = sheet.row(row)[7].value
        pk = sheet.row(row)[8].value

        if status == 'TRUE':
            status = True
        elif status == 'FALSE':
            status = False


        lista = Equipamento(name=nome, 
            modelo=modelo, 
            serial=serie, 
            patrimonio=patrimonio, 
            backup=status,
            setor=setor, 
            loja=Lojas.object.get(numero=filial), 
            obs=obs)
        aux.append(lista)
    
    #Equipamento.object.bulk_create(aux)



