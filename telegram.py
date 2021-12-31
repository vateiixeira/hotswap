from datetime import timedelta
from django.utils import timezone
from telethon import TelegramClient, events, sync
from telethon.tl import types
from telethon.tl.functions.contacts import ResolveUsernameRequest
import os,sys

import django
from django.conf import settings
from decouple import config

# if config('SYSTEM_TYPE') == 'linux':
#      sys.path.append('/root/betlol-api')
# else:
#      sys.path.append("C:\dev\api-bet")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_project.settings')
django.setup()

# Now this script or any imported module can use any part of Django it needs.

import django
from telethon import utils

django.setup()

from my_project.core.models import NotasSocin,ConfiguracaoSocin,ConfiguracaoEmail
from django.utils import timezone
from datetime import timedelta
from decouple import config
import redis

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
token_http = config('TOKEN_BOT','')

api_id = config('API_ID')
api_hash = config('API_SECRET')

client = TelegramClient('bot', api_id, api_hash).start(bot_token=token_http)
from time import sleep

#GRUPO = '-1274793802'


with client:
    real_id, peer_type = utils.resolve_id(-1274793802)
    redis_cli = redis.Redis(host='localhost', port=6379, db=0)
    print('Iniciando bot')
    wait_socin = 0
    wait_sessao = 0
    timeout_sessoes = False
    timeout_socin = False
    while True:
        notas = NotasSocin.objects.last()
        config = ConfiguracaoSocin.get_solo()
        configs_email = ConfiguracaoEmail.get_solo()
        configs_email.refresh_from_db()
        valor_sessao = redis_cli.get('sessoes-qtd').decode("utf-8")
        
        if int(valor_sessao) > 1 and not timeout_sessoes:
            msg = f'*** ALERTA ***\n SESSOES TRAVADAS \nQUANTIDADE: {valor_sessao}'
            client.send_message(types.PeerChannel(real_id),msg)
            timeout_sessoes = True
        
        if configs_email.telegram_notas_presas:
            #print(f'Habilitado,procurando notas...{config.quantidade_para_ativar_envio}/{notas.valor}')
            config.refresh_from_db()
            if notas and notas.valor >= config.quantidade_para_ativar_envio and notas.data + timedelta(minutes=3) > timezone.now()\
                    and not timeout_socin:
                #print('Nota encontrada,enviando...')
                msg = f'*** ALERTA ***\n NOTAS PRESAS SOCIN \nQUANTIDADE: {notas.valor}'
                client.send_message(types.PeerChannel(real_id),msg)
                timeout_socin = True
                sleep(300)
        
        if timeout_sessoes:
            wait_sessao += 10
        if timeout_socin:
            wait_socin += 10

        if wait_socin >= 300:
            timeout_socin = False
            wait_socin = 0
        if wait_sessao >= 300:
            timeout_sessoes = False
            wait_sessao = 0

        sleep(10)
        print('Não encontrou')


#client.log_out()
#client.run_until_disconnected()

# with client:
     # client.loop.run_until_complete(main())
