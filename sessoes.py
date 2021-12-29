
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_project.settings')
django.setup()

from my_project.core.conexao_oracle import Sessoes,stats
from my_project.core.models import ConfiguracaoSessoes,SessoesBlock
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.utils import timezone
from datetime import timedelta
from time import sleep
    
con = Sessoes()
blocks = {}
config = ConfiguracaoSessoes.get_solo()
channel_layer = get_channel_layer()
while True:
    config.refresh_from_db()
    data = con.run()
    if len(data['origem']) > 0:
        #print(data['bloqueados'])
        print(data['origem'])
        print(data['origem_data'])
        for lock in data['origem']:
            if blocks.get(lock,None):
                if blocks.get(lock,None)[0] + timedelta(minutes=config.minutos) < timezone.now():
                    if blocks.get(lock,None) and blocks.get(lock,None)[1]:
                        SessoesBlock.objects.get_or_create(
                            session_id =blocks[lock][1][stats['session_id']],
                            usuario =blocks[lock][1][stats['usuario']],
                            terminal =blocks[lock][1][stats['terminal']],
                            maquina =blocks[lock][1][stats['maquina']],
                            programa =blocks[lock][1][stats['programa']],
                            os_username =blocks[lock][1][stats['os']],
                            #sessao_bloqueada =blocks[lock][1][stats['sessao_bloqueada']],
                            data= blocks.get(lock,None)[0],
                        )
                        # aqui precisa ir pro channel no redis para notificar front e telegram
                    else:
                        print('Nao achou data para gravar o lock.')                            
            else:
                blocks[lock] = [timezone.now(),data['origem_data'].get(lock,None)]
        print(blocks)
        print('-'*50)
    else:
        blocks = {}
        # aqui precisa excluir channel para sair notificacao do front
    if data['origem_data']:
        msg = [
            {            
            'title': f"{data['origem_data'][x][3]} | {data['origem_data'][x][4]}",#"VILLEFORT\\ADM-CONTAB09",
            'description': f"{data['origem_data'][x][1]} - {data['origem_data'][x][5]}",#"ana.ferreira - ADM-CONTAB09",
            'done': False,
            } for x in data['origem_data']
        ]
    else:
        msg = []
    print('Executando')
    print(msg)
    qtd = len(data['bloqueados'])
    async_to_sync(channel_layer.group_send)(
                'sessoes',
                {'type': 'chat_message', 'message': msg, 'qtd': qtd}
            )
    sleep(10)